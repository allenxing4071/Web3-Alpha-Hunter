"""风险检测器"""

from typing import Dict, List
from loguru import logger
import re


class RiskDetector:
    """风险检测器 - 识别项目风险"""
    
    # 高风险关键词
    HIGH_RISK_KEYWORDS = [
        "guaranteed returns",
        "100x guaranteed",
        "risk-free",
        "get rich quick",
        "ponzi",
        "pyramid",
        "no risk",
        "guaranteed profit",
    ]
    
    # 中风险关键词
    MEDIUM_RISK_KEYWORDS = [
        "anonymous team",
        "team anonymous",
        "no audit",
        "unaudited",
        "large team allocation",
        "high tax",
    ]
    
    # 可疑模式
    SCAM_PATTERNS = [
        r"\d+x\s+guaranteed",  # "100x guaranteed"
        r"(send|deposit).*?(double|triple|multiply)",  # 发送钱翻倍
        r"first\s+\d+\s+get\s+bonus",  # 前XX名获得奖励
    ]
    
    def detect_risks(self, project_data: Dict) -> List[Dict]:
        """检测项目风险
        
        Args:
            project_data: 项目数据
            
        Returns:
            风险列表
        """
        risks = []
        text = str(project_data).lower()
        
        # 1. 检测高风险关键词
        for keyword in self.HIGH_RISK_KEYWORDS:
            if keyword in text:
                risks.append({
                    "type": "scam_indicator",
                    "severity": "high",
                    "message": f"检测到高风险关键词: '{keyword}'",
                    "category": "language"
                })
                logger.warning(f"🚨 HIGH RISK: Found keyword '{keyword}'")
        
        # 2. 检测中风险关键词
        for keyword in self.MEDIUM_RISK_KEYWORDS:
            if keyword in text:
                risks.append({
                    "type": "team_anonymous" if "anonymous" in keyword else "technical",
                    "severity": "medium",
                    "message": f"发现风险点: {keyword}",
                    "category": "transparency" if "anonymous" in keyword else "technical"
                })
        
        # 3. 检测可疑模式
        for pattern in self.SCAM_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                risks.append({
                    "type": "scam_pattern",
                    "severity": "high",
                    "message": f"检测到可疑模式: {pattern}",
                    "category": "pattern"
                })
                logger.warning(f"🚨 SCAM PATTERN detected: {pattern}")
        
        # 4. 检测团队透明度
        if "team" in project_data or "team_info" in project_data:
            team_info = project_data.get("team_info", "").lower()
            if "anonymous" in team_info or "anon" in team_info:
                risks.append({
                    "type": "team_anonymous",
                    "severity": "medium",
                    "message": "团队匿名,透明度不足",
                    "category": "transparency"
                })
        
        # 5. 检测审计状态
        if "audit" not in text and "audited" not in text:
            risks.append({
                "type": "no_audit",
                "severity": "medium",
                "message": "未发现审计信息",
                "category": "security"
            })
        
        # 6. 检测合约地址
        if "contracts" in project_data:
            contracts = project_data["contracts"]
            if not contracts or len(contracts) == 0:
                risks.append({
                    "type": "no_contract",
                    "severity": "low",
                    "message": "未找到合约地址",
                    "category": "technical"
                })
        
        logger.info(f"🔍 Risk detection completed: {len(risks)} risks found")
        return risks
    
    def calculate_scam_probability(self, risks: List[Dict]) -> float:
        """计算骗局概率
        
        Args:
            risks: 风险列表
            
        Returns:
            骗局概率 (0-100)
        """
        probability = 0.0
        
        # 按严重程度计算
        for risk in risks:
            if risk["severity"] == "high":
                probability += 30
            elif risk["severity"] == "medium":
                probability += 15
            elif risk["severity"] == "low":
                probability += 5
        
        # 如果有多个高风险,加倍
        high_risk_count = sum(1 for r in risks if r["severity"] == "high")
        if high_risk_count >= 2:
            probability *= 1.5
        
        return min(probability, 100)
    
    def calculate_risk_score(self, project_data: Dict) -> float:
        """计算风险控制评分(分数越高越安全)
        
        Args:
            project_data: 项目数据
            
        Returns:
            风险评分 (0-100)
        """
        score = 100.0  # 从满分开始扣分
        
        risks = self.detect_risks(project_data)
        
        # 根据风险扣分
        for risk in risks:
            if risk["severity"] == "high":
                score -= 30
            elif risk["severity"] == "medium":
                score -= 15
            elif risk["severity"] == "low":
                score -= 5
        
        # 正面因素加分
        text = str(project_data).lower()
        
        if "audit" in text or "audited" in text:
            score += 10
            logger.info("  +10分: 已审计")
        
        if "doxxed" in text or "公开团队" in text:
            score += 10
            logger.info("  +10分: 团队公开")
        
        if "certik" in text or "peckshield" in text:
            score += 5
            logger.info("  +5分: 知名审计机构")
        
        return max(min(score, 100), 0)
    
    def has_fatal_risk(self, risks: List[Dict]) -> bool:
        """是否存在致命风险
        
        Args:
            risks: 风险列表
            
        Returns:
            是否有致命风险
        """
        # 如果有2个以上高风险,视为致命
        high_risk_count = sum(1 for r in risks if r["severity"] == "high")
        
        if high_risk_count >= 2:
            logger.warning("⚠️ FATAL RISK: Multiple high-severity risks detected")
            return True
        
        # 检测特定致命风险
        for risk in risks:
            if risk["type"] == "scam_indicator":
                logger.warning(f"⚠️ FATAL RISK: {risk['message']}")
                return True
        
        return False


# 全局风险检测器实例
risk_detector = RiskDetector()

