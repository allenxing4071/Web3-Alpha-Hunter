"""项目评分服务"""

from typing import Dict, Optional
from loguru import logger


class ProjectScorer:
    """项目评分器"""
    
    # 各维度权重
    WEIGHTS = {
        "team": 0.20,        # 团队背景 20%
        "technology": 0.25,  # 技术创新 25%
        "community": 0.20,   # 社区热度 20%
        "tokenomics": 0.15,  # 代币模型 15%
        "market_timing": 0.10,  # 市场时机 10%
        "risk": 0.10,        # 风险控制 10%
    }
    
    def calculate_overall_score(
        self,
        team_score: float,
        tech_score: float,
        community_score: float,
        tokenomics_score: float,
        market_timing_score: float,
        risk_score: float,
        has_fatal_risk: bool = False,
        has_top_vc: bool = False
    ) -> float:
        """计算综合评分
        
        Args:
            team_score: 团队评分 (0-100)
            tech_score: 技术评分 (0-100)
            community_score: 社区评分 (0-100)
            tokenomics_score: 代币评分 (0-100)
            market_timing_score: 市场时机评分 (0-100)
            risk_score: 风险评分 (0-100)
            has_fatal_risk: 是否存在致命风险
            has_top_vc: 是否有顶级VC背书
            
        Returns:
            综合评分 (0-100)
        """
        
        # 加权平均
        overall = (
            team_score * self.WEIGHTS["team"] +
            tech_score * self.WEIGHTS["technology"] +
            community_score * self.WEIGHTS["community"] +
            tokenomics_score * self.WEIGHTS["tokenomics"] +
            market_timing_score * self.WEIGHTS["market_timing"] +
            risk_score * self.WEIGHTS["risk"]
        )
        
        # 致命风险降级
        if has_fatal_risk:
            logger.warning("Project has fatal risk, score reduced by 50%")
            overall *= 0.5
        
        # 顶级VC加分
        if has_top_vc:
            logger.info("Project has top-tier VC backing, +5 bonus")
            overall += 5
        
        # 确保在0-100范围内
        overall = min(max(overall, 0), 100)
        
        return round(overall, 2)
    
    def calculate_grade(self, score: float) -> str:
        """根据评分计算等级
        
        Args:
            score: 综合评分
            
        Returns:
            等级: S, A, B, C
        """
        if score >= 85:
            return "S"
        elif score >= 70:
            return "A"
        elif score >= 55:
            return "B"
        else:
            return "C"
    
    def score_team(self, data: Dict) -> float:
        """评估团队背景
        
        考虑因素:
        - LinkedIn背景质量
        - 过往项目成功率
        - 投资人质量
        """
        # TODO: 实现团队评分逻辑
        return 75.0
    
    def score_technology(self, data: Dict) -> float:
        """评估技术创新
        
        考虑因素:
        - 代码原创性
        - GitHub活跃度
        - 技术难度
        - 解决痛点程度
        """
        # TODO: 实现技术评分逻辑
        return 80.0
    
    def score_community(self, data: Dict) -> float:
        """评估社区热度
        
        考虑因素:
        - 粉丝增长速度
        - 互动质量
        - KOL提及频率
        """
        # TODO: 实现社区评分逻辑
        return 70.0
    
    def score_tokenomics(self, data: Dict) -> float:
        """评估代币模型
        
        考虑因素:
        - 流通机制合理性
        - 释放曲线
        - 实用场景
        """
        # TODO: 实现代币评分逻辑
        return 65.0
    
    def score_market_timing(self, data: Dict) -> float:
        """评估市场时机
        
        考虑因素:
        - 赛道热度
        - 叙事契合度
        - 竞品分析
        """
        # TODO: 实现市场时机评分逻辑
        return 75.0
    
    def score_risk(self, data: Dict) -> float:
        """评估风险控制
        
        考虑因素:
        - 合约审计情况
        - 团队透明度
        - 异常信号检测
        """
        # TODO: 实现风险评分逻辑
        return 80.0


# 全局评分器实例
project_scorer = ProjectScorer()

