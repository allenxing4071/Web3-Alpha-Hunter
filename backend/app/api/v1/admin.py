"""管理后台API"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import subprocess
import psutil

router = APIRouter(prefix="/admin", tags=["admin"])


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
    
    # 这里暂时返回模拟数据
    # 实际应该调用Celery任务
    
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
    
    # TODO: 实际调用Celery任务
    # from app.tasks.celery_app import celery_app
    # task = celery_app.send_task(task_name)
    
    return {
        "success": True,
        "source": source,
        "task_name": task_name,
        "message": f"数据采集任务已提交",
        "projects_found": 0,  # 模拟数据
        "note": "当前为模拟模式,实际需要Celery运行"
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

