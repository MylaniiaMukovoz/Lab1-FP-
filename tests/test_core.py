from core import make_processor
import copy

sample_usages = [
    {"id": 1, "minutes": 10, "sms": 5, "traffic_mb": 100, "tariff": "Test"}
]

dummy_tariff = lambda m, s, mb: m + s + (mb * 0.1)
dummy_bonus = lambda cost: cost

def test_referential_transparency():
    """Тест: однаковий вхід дає однаковий вихід"""
    processor = make_processor(dummy_tariff, dummy_bonus)
    
    result1 = processor(sample_usages)
    result2 = processor(sample_usages)
    
    assert result1 == result2

def test_no_mutation():
    """Тест: вхідні дані не змінюються"""
    processor = make_processor(dummy_tariff, dummy_bonus)
    original_data = copy.deepcopy(sample_usages)
    
    processor(sample_usages)
    
    assert sample_usages == original_data

def test_callable_policies():
    """Тест: перевірка правильності обчислень"""
    processor = make_processor(dummy_tariff, dummy_bonus)
    result = processor(sample_usages)
    
    records = result["records"]
    assert len(records) == 1
    assert records[0]["monthly_cost"] == 25.0
    assert result["revenue"] == 25.0