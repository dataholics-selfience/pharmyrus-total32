"""
BR Pending Inference Module
============================

Infere BRs pendentes baseado em WOs recentes
NUNCA cria patentes falsas - apenas sinaliza probabilidade
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger("pharmyrus.br_inference")


class BRPendingInference:
    """
    Infere BRs brasileiras pendentes baseado em WOs PCT recentes
    
    Lógica:
    - WO publicado → ~30 meses → entrada fase nacional BR
    - Depositantes conhecidos têm alta taxa de entrada
    - NÃO cria patentes falsas, apenas probabilidades
    """
    
    # Depositantes com alta taxa de entrada BR
    HIGH_PROBABILITY_DEPOSITORS = [
        'bayer', 'pfizer', 'novartis', 'roche', 'merck', 'sanofi',
        'astrazeneca', 'glaxosmithkline', 'gsk', 'takeda', 'abbvie',
        'johnson', 'eli lilly', 'bristol', 'gilead', 'amgen'
    ]
    
    def __init__(self):
        self.current_year = datetime.now().year
    
    def infer_pending_brs(
        self,
        wos: List[str],
        wo_details: List[Dict],
        found_brs: List[str]
    ) -> List[Dict]:
        """
        Infere BRs pendentes baseado em WOs recentes
        
        Args:
            wos: Lista de números WO
            wo_details: Detalhes dos WOs (applicants, dates)
            found_brs: BRs já encontradas (para evitar duplicatas)
        
        Returns:
            Lista de inferências de BRs pendentes
        """
        pending_inferences = []
        found_br_set = set(self._normalize_br(br) for br in found_brs)
        
        for wo in wos:
            # Extrair ano do WO
            wo_year = self._extract_wo_year(wo)
            
            if not wo_year or wo_year < 2023:
                continue  # Só WOs recentes
            
            # Buscar detalhes do WO
            wo_info = self._find_wo_details(wo, wo_details)
            
            # Gerar padrão BR esperado
            br_expected = self._generate_br_pattern(wo, wo_year)
            
            # Verificar se já foi encontrado
            if self._normalize_br(br_expected) in found_br_set:
                continue  # Já publicado
            
            # Calcular probabilidade
            probability = self._calculate_probability(wo_year, wo_info)
            
            if probability == 'NONE':
                continue  # Não vale a pena inferir
            
            # Criar inferência
            inference = {
                'type': 'INFERRED_PENDING',
                'br_expected': br_expected,
                'wo_source': wo,
                'wo_year': wo_year,
                'applicant': wo_info.get('applicant', 'Unknown'),
                'expected_publication_year': wo_year + 2,  # PCT + ~30 meses
                'probability': probability,
                'status': 'NOT_YET_PUBLISHED',
                'confidence_score': self._probability_to_score(probability),
                'warning': '⚠️ INFERENCE ONLY - Not a confirmed published patent'
            }
            
            pending_inferences.append(inference)
        
        logger.info(f"   🔮 Inferred {len(pending_inferences)} pending BRs from recent WOs")
        
        return pending_inferences
    
    def _extract_wo_year(self, wo: str) -> Optional[int]:
        """Extrai ano do número WO"""
        match = re.search(r'WO(\d{4})', wo, re.I)
        if match:
            return int(match.group(1))
        return None
    
    def _find_wo_details(self, wo: str, wo_details: List[Dict]) -> Dict:
        """Busca detalhes do WO na lista"""
        wo_normalized = wo.upper().replace('/', '').replace(' ', '')
        
        for detail in wo_details:
            detail_number = detail.get('patent_number', '').upper().replace('/', '').replace(' ', '')
            if detail_number == wo_normalized:
                return detail
        
        return {}
    
    def _generate_br_pattern(self, wo: str, wo_year: int) -> str:
        """
        Gera padrão de BR esperado
        
        WO2024123456 → BR112026XXXXXX
        (ano WO + 2 = ano BR)
        """
        br_year = wo_year + 2
        
        # Se já passou do ano esperado, pode ter atrasado
        if br_year < self.current_year:
            br_year = self.current_year
        
        return f"BR112{br_year % 100:02d}XXXXXX"
    
    def _calculate_probability(self, wo_year: int, wo_info: Dict) -> str:
        """
        Calcula probabilidade de entrada BR
        
        Returns:
            'HIGH', 'MEDIUM', 'LOW', 'NONE'
        """
        # WO muito antigo
        if wo_year < 2023:
            return 'NONE'
        
        # WO muito recente (ainda no prazo PCT)
        time_since_wo = self.current_year - wo_year
        
        if time_since_wo < 1:
            return 'LOW'  # Muito cedo
        
        # Verificar depositante
        applicant = wo_info.get('applicant', '').lower()
        
        is_high_prob = any(
            dep in applicant 
            for dep in self.HIGH_PROBABILITY_DEPOSITORS
        )
        
        # Regras de probabilidade
        if is_high_prob and time_since_wo >= 2:
            return 'HIGH'  # Depositante conhecido + tempo suficiente
        elif is_high_prob:
            return 'MEDIUM'  # Depositante conhecido, mas cedo
        elif time_since_wo >= 2:
            return 'MEDIUM'  # Tempo suficiente, mas depositante desconhecido
        else:
            return 'LOW'
    
    def _probability_to_score(self, probability: str) -> float:
        """Converte probabilidade em score numérico"""
        scores = {
            'HIGH': 0.9,
            'MEDIUM': 0.6,
            'LOW': 0.3,
            'NONE': 0.0
        }
        return scores.get(probability, 0.0)
    
    def _normalize_br(self, br: str) -> str:
        """Normaliza número BR"""
        if not br:
            return ""
        return re.sub(r'[\s\-/X]', '', br.upper())
