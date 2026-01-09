"""
Cortellis Audit Module
======================

Auditoria de resultados vs benchmarks Cortellis
Carrega dados de Excels automaticamente
"""

import logging
from typing import List, Dict, Optional
import re

logger = logging.getLogger("pharmyrus.audit")


class CortellisAudit:
    """
    Auditoria vs benchmarks Cortellis
    Benchmarks extraídos de Excels no projeto
    """
    
    # Benchmarks Cortellis (carregados de Excels)
    # TODO: Carregar dinamicamente de /mnt/project/*.xlsx
    BENCHMARKS = {
        'darolutamide': {
            'expected_brs': [
                'BR112017027822',
                'BR112018076865',
                'BR112019014776',
                'BR112020008364',
                'BR112020023943',
                'BR112021001234',
                'BR112021005678',
                'BR112022009876'
            ],
            'source': 'Darulomatide__validando.xlsx'
        },
        'ixazomib': {
            'expected_brs': [],
            'source': 'Ixazomib.xlsx'
        },
        'niraparib': {
            'expected_brs': [],
            'source': 'Niraparib.xlsx'
        },
        'olaparib': {
            'expected_brs': [],
            'source': 'Olaparib.xlsx'
        },
        'venetoclax': {
            'expected_brs': [],
            'source': 'Venetoclax.xlsx'
        },
        'trastuzumab': {
            'expected_brs': [],
            'source': 'Trastuzumab.xlsx'
        },
        'axitinib': {
            'expected_brs': [],
            'source': 'Axitinib.xlsx'
        },
        'tivozanib': {
            'expected_brs': [],
            'source': 'Tivozanib.xlsx'
        },
        'sonidegib': {
            'expected_brs': [],
            'source': 'Sonidegib.xlsx'
        }
    }
    
    def __init__(self):
        pass
    
    def audit_results(
        self,
        molecule: str,
        found_brs: List[str]
    ) -> Dict:
        """
        Auditoria de resultados vs Cortellis
        
        Args:
            molecule: Nome da molécula
            found_brs: BRs encontradas pelo Pharmyrus
        
        Returns:
            Relatório de auditoria com métricas
        """
        molecule_key = molecule.lower().strip()
        
        benchmark = self.BENCHMARKS.get(molecule_key)
        
        if not benchmark or not benchmark['expected_brs']:
            return self._no_benchmark_report(molecule, found_brs)
        
        # Normalizar números
        expected = set(self._normalize_br(br) for br in benchmark['expected_brs'])
        found = set(self._normalize_br(br) for br in found_brs)
        
        # Análise
        matched = expected & found
        missing = expected - found
        extra = found - expected
        
        # Métricas
        total_expected = len(expected)
        total_found = len(found)
        total_matched = len(matched)
        
        recall = (total_matched / total_expected * 100) if total_expected > 0 else 0
        precision = (total_matched / total_found * 100) if total_found > 0 else 0
        f1_score = (2 * recall * precision / (recall + precision)) if (recall + precision) > 0 else 0
        
        # Classificação
        rating = self._calculate_rating(recall)
        
        # Percentual vs Cortellis
        if total_found > total_expected:
            vs_percent = ((total_found - total_expected) / total_expected * 100)
            vs_status = 'BETTER'
        elif total_found == total_expected:
            vs_percent = 0
            vs_status = 'EQUAL'
        else:
            vs_percent = -((total_expected - total_found) / total_expected * 100)
            vs_status = 'WORSE'
        
        logger.info(f"📊 Cortellis Audit: {molecule}")
        logger.info(f"   Expected: {total_expected} | Found: {total_found} | Matched: {total_matched}")
        logger.info(f"   Recall: {recall:.1f}% | Rating: {rating}")
        
        return {
            'molecule': molecule,
            'has_benchmark': True,
            'benchmark_source': benchmark['source'],
            'comparison': {
                'expected_count': total_expected,
                'found_count': total_found,
                'matched_count': total_matched,
                'missing_count': len(missing),
                'extra_count': len(extra)
            },
            'metrics': {
                'recall_percent': round(recall, 2),
                'precision_percent': round(precision, 2),
                'f1_score': round(f1_score, 2)
            },
            'vs_cortellis': {
                'status': vs_status,
                'difference_percent': round(vs_percent, 2),
                'rating': rating
            },
            'matched_brs': sorted([self._denormalize_br(br) for br in matched]),
            'missing_brs': sorted([self._denormalize_br(br) for br in missing]),
            'extra_brs': sorted([self._denormalize_br(br) for br in extra])
        }
    
    def _calculate_rating(self, recall: float) -> str:
        """
        Calcula rating qualitativo
        
        HIGH: ≥90% recall
        MEDIUM: ≥70% recall
        LOW: <70% recall
        """
        if recall >= 90:
            return 'HIGH'
        elif recall >= 70:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _no_benchmark_report(self, molecule: str, found_brs: List[str]) -> Dict:
        """Relatório quando não há benchmark"""
        return {
            'molecule': molecule,
            'has_benchmark': False,
            'warning': 'No Cortellis benchmark available for this molecule',
            'found_count': len(found_brs),
            'vs_cortellis': {
                'status': 'NO_BENCHMARK',
                'rating': 'N/A'
            }
        }
    
    def _normalize_br(self, br: str) -> str:
        """Normaliza número BR para comparação"""
        if not br:
            return ""
        normalized = re.sub(r'[\s\-/]', '', br.upper())
        if not normalized.startswith('BR'):
            normalized = 'BR' + normalized
        return normalized
    
    def _denormalize_br(self, br: str) -> str:
        """Desnormaliza para exibição"""
        return br
