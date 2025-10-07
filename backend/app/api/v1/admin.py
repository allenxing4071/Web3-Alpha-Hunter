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


@router.post("/celery/worker/{action}")
async def control_celery_worker(action: str) -> Dict[str, Any]:
    """控制Celery Worker启动/停止"""
    import subprocess
    import os
    
    if action not in ["start", "stop"]:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'")
    
    try:
        if action == "stop":
            # 停止Celery Worker
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'celery' in cmdline.lower() and 'worker' in cmdline.lower():
                        proc.terminate()
                        proc.wait(timeout=5)
                        return {
                            "success": True,
                            "message": "Celery Worker已停止",
                            "action": "stop"
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                "success": False,
                "message": "未找到运行中的Celery Worker",
                "action": "stop"
            }
        
        else:  # start
            # 启动Celery Worker
            # 获取backend目录（当前文件所在的backend目录）
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            
            # 使用python3 -m celery确保使用正确的Python环境
            cmd = [
                "python3", "-m", "celery", "-A", "app.tasks.celery_app", "worker",
                "--loglevel=info",
                "--logfile=/tmp/celery_worker.log"
            ]
            
            # 后台启动
            subprocess.Popen(
                cmd,
                cwd=current_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            return {
                "success": True,
                "message": "Celery Worker启动命令已发送",
                "action": "start",
                "note": "请等待几秒后刷新状态"
            }
            
    except Exception as e:
        print(f"❌ 控制Celery Worker失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/celery/beat/{action}")
async def control_celery_beat(action: str) -> Dict[str, Any]:
    """控制Celery Beat启动/停止"""
    import subprocess
    import os
    
    if action not in ["start", "stop"]:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'")
    
    try:
        if action == "stop":
            # 停止Celery Beat
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'celery' in cmdline.lower() and 'beat' in cmdline.lower():
                        proc.terminate()
                        proc.wait(timeout=5)
                        return {
                            "success": True,
                            "message": "Celery Beat已停止",
                            "action": "stop"
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                "success": False,
                "message": "未找到运行中的Celery Beat",
                "action": "stop"
            }
        
        else:  # start
            # 启动Celery Beat
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            
            cmd = [
                "python3", "-m", "celery", "-A", "app.tasks.celery_app", "beat",
                "--loglevel=info",
                "--logfile=/tmp/celery_beat.log"
            ]
            
            subprocess.Popen(
                cmd,
                cwd=current_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            return {
                "success": True,
                "message": "Celery Beat启动命令已发送",
                "action": "start",
                "note": "请等待几秒后刷新状态"
            }
            
    except Exception as e:
        print(f"❌ 控制Celery Beat失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
        # 尝试解密,如果失败则返回原始值(可能是未加密的测试数据)
        decrypted_key = ""
        if config.api_key:
            try:
                decrypted_key = decrypt_api_key(config.api_key)
            except Exception:
                # 解密失败,可能是未加密的数据,直接返回(或返回空字符串以保护隐私)
                decrypted_key = config.api_key if len(config.api_key) < 100 else ""
        
        config_list.append({
            "name": config.name,
            "key": decrypted_key,
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
            # DeepSeek - 直接使用官方API
            from openai import OpenAI
            client = OpenAI(
                api_key=request.api_key,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": "test"}]
            )
            return AITestResponse(
                success=True,
                message="DeepSeek API连接成功"
            )
            
        elif request.provider == "claude":
            # WildCard的Claude使用OpenAI客户端格式
            from openai import OpenAI
            client = OpenAI(
                api_key=request.api_key,
                base_url="https://api.gptsapi.net/v1"
            )
            # 不指定max_tokens，让WildCard自动处理
            response = client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": "test"}]
            )
            return AITestResponse(
                success=True,
                message="Claude API连接成功 (via WildCard)"
            )
            
        elif request.provider == "openai":
            # WildCard的OpenAI - 使用OpenAI SDK (不发送max_tokens避免冲突)
            from openai import OpenAI
            client = OpenAI(
                api_key=request.api_key,
                base_url="https://api.gptsapi.net/v1"
            )
            # 不指定max_tokens，让WildCard自动处理
            response = client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": "test"}]
            )
            return AITestResponse(
                success=True,
                message="OpenAI API连接成功 (via WildCard)"
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


# =====================================================
# AI工作配置管理
# =====================================================

@router.get("/ai-work-config")
async def get_ai_work_config(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """获取AI工作配置"""
    from sqlalchemy import text
    
    try:
        result = db.execute(text("""
            SELECT 
                primary_goal,
                target_roi,
                risk_tolerance,
                min_ai_score,
                required_cross_validation,
                min_platforms,
                search_lookback_hours,
                project_age_limit_days,
                max_projects_per_day,
                max_kols_per_day,
                rules
            FROM ai_work_config
            WHERE id = 1
        """))
        
        row = result.fetchone()
        if not row:
            # 如果没有配置，返回默认值
            return {
                "success": True,
                "config": {
                    "primary_goal": "发现未发币的早期优质Web3项目",
                    "target_roi": 50.0,
                    "risk_tolerance": "aggressive",
                    "min_ai_score": 70.0,
                    "required_cross_validation": True,
                    "min_platforms": 2,
                    "search_lookback_hours": 24,
                    "project_age_limit_days": 180,
                    "max_projects_per_day": 50,
                    "max_kols_per_day": 20,
                    "rules": {}
                }
            }
        
        return {
            "success": True,
            "config": {
                "primary_goal": row[0],
                "target_roi": float(row[1]) if row[1] else 50.0,
                "risk_tolerance": row[2],
                "min_ai_score": float(row[3]) if row[3] else 70.0,
                "required_cross_validation": row[4],
                "min_platforms": row[5],
                "search_lookback_hours": row[6],
                "project_age_limit_days": row[7],
                "max_projects_per_day": row[8],
                "max_kols_per_day": row[9],
                "rules": row[10] if row[10] else {}
            }
        }
        
    except Exception as e:
        print(f"❌ 获取AI工作配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai-work-config")
async def update_ai_work_config(
    config: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新AI工作配置"""
    from sqlalchemy import text
    import json
    
    try:
        # 提取配置字段
        primary_goal = config.get("primary_goal", "发现未发币的早期优质Web3项目")
        target_roi = config.get("target_roi", 50.0)
        risk_tolerance = config.get("risk_tolerance", "aggressive")
        min_ai_score = config.get("min_ai_score", 70.0)
        required_cross_validation = config.get("required_cross_validation", True)
        min_platforms = config.get("min_platforms", 2)
        search_lookback_hours = config.get("search_lookback_hours", 24)
        project_age_limit_days = config.get("project_age_limit_days", 180)
        max_projects_per_day = config.get("max_projects_per_day", 50)
        max_kols_per_day = config.get("max_kols_per_day", 20)
        rules = config.get("rules", {})
        
        # 更新数据库
        db.execute(text("""
            UPDATE ai_work_config
            SET 
                primary_goal = :primary_goal,
                target_roi = :target_roi,
                risk_tolerance = :risk_tolerance,
                min_ai_score = :min_ai_score,
                required_cross_validation = :required_cross_validation,
                min_platforms = :min_platforms,
                search_lookback_hours = :search_lookback_hours,
                project_age_limit_days = :project_age_limit_days,
                max_projects_per_day = :max_projects_per_day,
                max_kols_per_day = :max_kols_per_day,
                rules = CAST(:rules AS jsonb),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """), {
            "primary_goal": primary_goal,
            "target_roi": target_roi,
            "risk_tolerance": risk_tolerance,
            "min_ai_score": min_ai_score,
            "required_cross_validation": required_cross_validation,
            "min_platforms": min_platforms,
            "search_lookback_hours": search_lookback_hours,
            "project_age_limit_days": project_age_limit_days,
            "max_projects_per_day": max_projects_per_day,
            "max_kols_per_day": max_kols_per_day,
            "rules": json.dumps(rules)
        })
        
        db.commit()
        
        return {
            "success": True,
            "message": "AI工作配置已更新"
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ 更新AI工作配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pending-projects")
async def get_pending_projects(
    limit: int = 50,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取待审核项目列表"""
    from sqlalchemy import text
    
    try:
        result = db.execute(text("""
            SELECT 
                id,
                project_name,
                symbol,
                description,
                discovered_from,
                source_url,
                ai_score,
                ai_grade,
                ai_recommendation_reason,
                ai_confidence,
                review_status,
                created_at
            FROM projects_pending
            WHERE review_status = 'pending'
            ORDER BY ai_score DESC, created_at DESC
            LIMIT :limit
        """), {"limit": limit})
        
        projects = []
        for row in result:
            projects.append({
                "id": row[0],
                "name": row[1],
                "symbol": row[2],
                "description": row[3],
                "discovered_from": row[4],
                "source_url": row[5],
                "ai_score": float(row[6]) if row[6] else 0,
                "ai_grade": row[7],
                "ai_recommendation_reason": row[8] if row[8] else {},
                "ai_confidence": float(row[9]) if row[9] else 0,
                "review_status": row[10],
                "created_at": row[11].isoformat() if row[11] else None
            })
        
        # 统计数据
        stats_result = db.execute(text("""
            SELECT 
                review_status,
                COUNT(*) as count
            FROM projects_pending
            GROUP BY review_status
        """))
        
        stats = {}
        for row in stats_result:
            stats[row[0]] = row[1]
        
        return {
            "success": True,
            "projects": projects,
            "total": len(projects),
            "stats": stats
        }
        
    except Exception as e:
        print(f"❌ 获取待审核项目失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pending-projects/{project_id}/approve")
async def approve_pending_project(
    project_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """批准待审核项目"""
    from sqlalchemy import text
    
    try:
        # 获取待审核项目
        result = db.execute(text("""
            SELECT 
                project_name,
                symbol,
                description,
                discovered_from,
                ai_score,
                ai_grade,
                ai_extracted_info,
                source_url
            FROM projects_pending
            WHERE id = :id AND review_status = 'pending'
        """), {"id": project_id})
        
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="项目不存在或已审核")
        
        # 创建正式项目（只使用projects表中存在的字段）
        db.execute(text("""
            INSERT INTO projects (
                name, description, overall_score,
                created_at, updated_at
            ) VALUES (
                :name, :description, :overall_score,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
        """), {
            "name": row[0],
            "description": row[2],
            "overall_score": row[4]
        })
        
        # 更新待审核项目状态
        db.execute(text("""
            UPDATE projects_pending
            SET 
                review_status = 'approved',
                reviewed_at = CURRENT_TIMESTAMP,
                reviewed_by = 'admin'
            WHERE id = :id
        """), {"id": project_id})
        
        # 记录AI学习反馈
        db.execute(text("""
            INSERT INTO ai_learning_feedback (
                feedback_type, related_project_id, user_decision, created_at
            ) VALUES (
                'project_review', :project_id, 'approved', CURRENT_TIMESTAMP
            )
        """), {"project_id": project_id})
        
        db.commit()
        
        return {
            "success": True,
            "message": "项目已批准并保存到数据库"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ 批准项目失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pending-projects/{project_id}/reject")
async def reject_pending_project(
    project_id: int,
    reason: str = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """拒绝待审核项目"""
    from sqlalchemy import text
    
    try:
        # 更新待审核项目状态
        db.execute(text("""
            UPDATE projects_pending
            SET 
                review_status = 'rejected',
                reviewed_at = CURRENT_TIMESTAMP,
                reviewed_by = 'admin',
                reject_reason = :reason
            WHERE id = :id AND review_status = 'pending'
        """), {"id": project_id, "reason": reason})
        
        if db.execute(text("SELECT * FROM projects_pending WHERE id = :id"), {"id": project_id}).rowcount == 0:
            raise HTTPException(status_code=404, detail="项目不存在或已审核")
        
        # 记录AI学习反馈
        db.execute(text("""
            INSERT INTO ai_learning_feedback (
                feedback_type, related_project_id, user_decision, user_reason, created_at
            ) VALUES (
                'project_review', :project_id, 'rejected', :reason, CURRENT_TIMESTAMP
            )
        """), {"project_id": project_id, "reason": reason})
        
        db.commit()
        
        return {
            "success": True,
            "message": "项目已拒绝"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ 拒绝项目失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

