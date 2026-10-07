from typing import Callable, TypedDict, List, Dict

class Usage(TypedDict):
    id: int
    minutes: int
    sms: int
    traffic_mb: float
    tariff: str

class BilledUsage(TypedDict):
    id: int
    minutes: int
    sms: int
    traffic_mb: float
    tariff: str
    monthly_cost: float

TariffFn = Callable[[int, int, float], float]  
BonusFn = Callable[[float], float]             

def with_cost(usage: Usage, cost: float) -> BilledUsage:
    """Створює новий запис з доданою ціною (без мутації вхідного словника)"""
    new_usage = dict(usage) 
    new_usage["monthly_cost"] = cost
    return new_usage

def make_processor(
    calculate_base_cost: TariffFn,
    apply_bonus: BonusFn
) -> Callable[[List[Usage]], Dict[str, object]]:
    """Фабрика, яка створює готову функцію для обробки даних"""
    
    def process(usages: List[Usage]) -> Dict[str, object]:
        processed_records = []
        total_revenue = 0.0
        
        for u in usages:
            base_cost = calculate_base_cost(u["minutes"], u["sms"], u["traffic_mb"])
            
            final_cost = apply_bonus(base_cost)
            
            new_u = with_cost(u, final_cost)
            processed_records.append(new_u)
            
            total_revenue += final_cost
            
        return {
            "count": len(processed_records), 
            "revenue": total_revenue, 
            "records": processed_records
        }
    
    return process