"""管理后台API"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from sqlalchemy.orm import Session
import subprocess
import psutil
import uuid
from cryptography.fernet import Fernet
import base64
import hashlib

from app.db.session import get_db
from app.models.ai_config import AIConfig
from app.schemas.ai_config import (
    AIConfigBase, AIConfigResponse, AITestRequest, AITestResponse
)

router = APIRouter(prefix="/admin", tags=["admin"])

# 密钥加密密钥(实际使用时应从环境变量读取)
ENCRYPTION_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"web3-alpha-hunter-secret-key").digest())
cipher_suite = Fernet(ENCRYPTION_KEY)


def encrypt_api_key(api_key: str) -> str:
    """加密API密钥"""
    return cipher_suite.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """解密API密钥"""
    return cipher_suite.decrypt(encrypted_key.encode()).decode()


@router.get("/celery-status")
async def get_celery_status() -> Dict[str, Any]:
    """检查Celery Worker和Beat运行状态"""
    
    worker_running = False
    beat_running = False
    
    try:
        # 检查进程是否在运行
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                
                if 'celery' in cmdline.lower() and 'worker' in cmdline.lower():
                    worker_running = True
                    
                if 'celery' in cmdline.lower() and 'beat' in cmdline.lower():
                    beat_running = True
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except Exception as e:
        print(f"Error checking Celery status: {e}")
    
    return {
        "worker_running": worker_running,
        "beat_running": beat_running,
        "auto_update_enabled": worker_running and beat_running
    }


@router.post("/collect/{source}")
async def trigger_collection(source: str) -> Dict[str, Any]:
    """手动触发数据采集
    
    Args:
        source: 数据源 (twitter, telegram, coingecko, all)
    """
    
    if source == "twitter":
        task_name = "app.tasks.collectors.collect_twitter_data"
    elif source == "telegram":
        task_name = "app.tasks.collectors.collect_telegram_data"
    elif source == "coingecko":
        task_name = "app.tasks.collectors.collect_coingecko_data"
    elif source == "all":
        task_name = "app.tasks.collectors.collect_all_sources"
    else:
        raise HTTPException(status_code=400, detail="Invalid source")
    
    # 检查Celery是否运行
    try:
        from app.tasks.celery_app import celery_app
        
        # 尝试调用Celery任务
        task = celery_app.send_task(task_name)
        
        return {
            "success": True,
            "source": source,
            "task_id": task.id,
            "task_name": task_name,
            "message": f"{source}数据采集任务已提交到队列",
            "status": "pending",
            "note": "任务已发送,请等待Celery Worker执行"
        }
        
    except Exception as e:
        # Celery未运行,使用同步方式直接执行
        try:
            if source == "all":
                from app.tasks.collectors import collect_all_sources
                result = collect_all_sources()
            elif source == "twitter":
                from app.tasks.collectors import collect_twitter_data
                result = collect_twitter_data()
            elif source == "telegram":
                from app.tasks.collectors import collect_telegram_data
                result = collect_telegram_data()
            else:
                result = {"success": False, "error": "Unsupported source"}
            
            return {
                "success": result.get("success", True),
                "source": source,
                "projects_found": result.get("projects_found", result.get("total_projects", 0)),
                "message": f"{source}采集完成(同步模式)",
                "note": "Celery未运行,已使用同步执行",
                "details": result
            }
            
        except Exception as exec_error:
            return {
                "success": False,
                "source": source,
                "message": f"采集失败: {str(exec_error)}",
                "projects_found": 0,
                "note": "请检查Celery配置或后端日志"
            }


@router.get("/tasks/status")
async def get_tasks_status() -> Dict[str, Any]:
    """获取所有定时任务状态"""
    
    # TODO: 从Celery获取实际任务状态
    
    return {
        "tasks": [
            {
                "name": "Twitter数据采集",
                "schedule": "每5分钟",
                "status": "pending",
                "last_run": None,
                "next_run": None
            },
            {
                "name": "Telegram数据采集",
                "schedule": "每15分钟",
                "status": "pending",
                "last_run": None,
                "next_run": None
            },
            {
                "name": "AI项目分析",
                "schedule": "每1小时",
                "status": "pending",
                "last_run": None,
                "next_run": None
            },
            {
                "name": "每日Alpha报告",
                "schedule": "每天09:00",
                "status": "pending",
                "last_run": None,
                "next_run": None
            }
        ]
    }


# ==================== AI配置管理 ====================

@router.post("/ai-configs")
async def save_ai_configs(
    configs_data: Dict[str, List[AIConfigBase]],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """保存AI配置到数据库(加密存储)"""
    
    configs = configs_data.get("configs", [])
    saved_count = 0
    
    for config_data in configs:
        # 查找或创建配置
        config = db.query(AIConfig).filter(
            AIConfig.name == config_data.name
        ).first()
        
        if config:
            # 更新现有配置
            if config_data.key:  # 只有当有密钥时才更新
                config.api_key = encrypt_api_key(config_data.key)
            config.enabled = config_data.enabled
            config.model = config_data.model
        else:
            # 创建新配置
            if not config_data.key:
                continue  # 跳过没有密钥的配置
                
            config = AIConfig(
                id=str(uuid.uuid4()),
                name=config_data.name,
                api_key=encrypt_api_key(config_data.key),
                enabled=config_data.enabled,
                model=config_data.model
            )
            db.add(config)
        
        saved_count += 1
    
    db.commit()
    
    return {
        "success": True,
        "message": f"已保存{saved_count}个AI配置",
        "saved_count": saved_count
    }


@router.get("/ai-configs")
async def get_ai_configs(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """获取AI配置(不返回密钥原文)"""
    
    configs = db.query(AIConfig).all()
    
    config_list = []
    for config in configs:
        config_list.append({
            "name": config.name,
            "key": decrypt_api_key(config.api_key) if config.api_key else "",  # 解密返回
            "enabled": config.enabled,
            "model": config.model
        })
    
    return {
        "success": True,
        "configs": config_list
    }


@router.post("/test-ai")
async def test_ai_connection(request: AITestRequest) -> AITestResponse:
    """测试AI API连接"""
    
    try:
        if request.provider == "deepseek":
            from openai import OpenAI
            client = OpenAI(
                api_key=request.api_key,
                base_url="https://api.deepseek.com"
            )
            # 简单测试请求
            response = client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            return AITestResponse(
                success=True,
                message="DeepSeek API连接成功"
            )
            
        elif request.provider == "claude":
            from anthropic import Anthropic
            client = Anthropic(api_key=request.api_key)
            response = client.messages.create(
                model=request.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return AITestResponse(
                success=True,
                message="Claude API连接成功"
            )
            
        elif request.provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=request.api_key)
            response = client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            return AITestResponse(
                success=True,
                message="OpenAI API连接成功"
            )
            
        else:
            return AITestResponse(
                success=False,
                error="不支持的AI提供商"
            )
            
    except Exception as e:
        error_msg = str(e)
        return AITestResponse(
            success=False,
            error=f"API连接失败: {error_msg}"
        )

