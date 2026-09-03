"""Test suite for the FineCalculator service."""

import pytest
from services.fine_calculator import FineCalculator
from models.exceptions import FineCalculationError


class TestFineCalculator:
    """Test suite for FineCalculator service."""
    
    def test_initialization_with_default_rate(self) -> None:
        """Test FineCalculator initializes with default rate."""
        calc = FineCalculator()
        assert calc.daily_fine_rate == 50.0
    
    def test_initialization_with_custom_rate(self) -> None:
        """Test FineCalculator initializes with custom rate."""
        calc = FineCalculator(daily_fine_rate=75.0)
        assert calc.daily_fine_rate == 75.0
    
    def test_initialization_with_invalid_rate(self) -> None:
        """Test FineCalculator raises error for non-positive rate."""
        with pytest.raises(FineCalculationError):
            FineCalculator(daily_fine_rate=0)
        
        with pytest.raises(FineCalculationError):
            FineCalculator(daily_fine_rate=-10.0)
    
    def test_calculate_overdue_fine_no_days_overdue(self) -> None:
        """Test fine calculation when book is returned on time."""
        calc = FineCalculator()
        due_date_payload = {'date': '2024-01-15T00:00:00'}
        return_date_payload = {'date': '2024-01-15T00:00:00'}
        
        fine = calc.calculate_overdue_fine(due_date_payload, return_date_payload)
        assert fine == 0.0
    
    def test_calculate_overdue_fine_with_days_overdue(self) -> None:
        """Test fine calculation with overdue days."""
        calc = FineCalculator(daily_fine_rate=50.0)
        due_date_payload = {'date': '2024-01-15T00:00:00'}
        return_date_payload = {'date': '2024-01-20T00:00:00'}
        
        fine = calc.calculate_overdue_fine(due_date_payload, return_date_payload)
        assert fine == 250.0  # 5 days * 50
    
    def test_calculate_overdue_fine_early_return(self) -> None:
        """Test fine calculation when book is returned early."""
        calc = FineCalculator()
        due_date_payload = {'date': '2024-01-20T00:00:00'}
        return_date_payload = {'date': '2024-01-15T00:00:00'}
        
        fine = calc.calculate_overdue_fine(due_date_payload, return_date_payload)
        assert fine == 0.0
    
    def test_calculate_overdue_fine_current_date(self) -> None:
        """Test fine calculation using current date."""
        calc = FineCalculator(daily_fine_rate=10.0)
        due_date_payload = {'date': '2020-01-01T00:00:00'}
        
        fine = calc.calculate_overdue_fine(due_date_payload)
        assert fine > 0
    
    def test_calculate_overdue_fine_invalid_due_date(self) -> None:
        """Test error handling for invalid due date."""
        calc = FineCalculator()
        due_date_payload = {'date': 'invalid-date'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_overdue_fine(due_date_payload)
    
    def test_calculate_overdue_fine_missing_date_key(self) -> None:
        """Test error handling when 'date' key is missing."""
        calc = FineCalculator()
        due_date_payload = {'invalid_key': '2024-01-15T00:00:00'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_overdue_fine(due_date_payload)
    
    def test_calculate_member_total_fine_no_additional(self) -> None:
        """Test total fine calculation with only accumulated fines."""
        calc = FineCalculator()
        member_payload = {'accumulated_fines': 100.0, 'member_id': 'M1'}
        
        total = calc.calculate_member_total_fine(member_payload)
        assert total == 100.0
    
    def test_calculate_member_total_fine_with_additional(self) -> None:
        """Test total fine calculation with additional charges."""
        calc = FineCalculator()
        member_payload = {'accumulated_fines': 100.0, 'member_id': 'M1'}
        
        total = calc.calculate_member_total_fine(member_payload, additional_charges=50.0)
        assert total == 150.0
    
    def test_calculate_member_total_fine_invalid_payload(self) -> None:
        """Test error handling for invalid member payload."""
        calc = FineCalculator()
        
        with pytest.raises(FineCalculationError):
            calc.calculate_member_total_fine("not a dict")
    
    def test_calculate_member_total_fine_missing_accumulated_fines(self) -> None:
        """Test error handling when accumulated_fines key is missing."""
        calc = FineCalculator()
        member_payload = {'member_id': 'M1'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_member_total_fine(member_payload)
    
    def test_calculate_member_total_fine_negative_accumulated(self) -> None:
        """Test error handling for negative accumulated fines."""
        calc = FineCalculator()
        member_payload = {'accumulated_fines': -50.0, 'member_id': 'M1'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_member_total_fine(member_payload)
    
    def test_calculate_member_total_fine_negative_additional(self) -> None:
        """Test error handling for negative additional charges."""
        calc = FineCalculator()
        member_payload = {'accumulated_fines': 100.0, 'member_id': 'M1'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_member_total_fine(member_payload, additional_charges=-50.0)
    
    def test_apply_fine_cap_below_cap(self) -> None:
        """Test fine cap when fine is below the cap."""
        calc = FineCalculator()
        fine = calc.apply_fine_cap(100.0)
        assert fine == 100.0
    
    def test_apply_fine_cap_exceeds_cap(self) -> None:
        """Test fine cap when fine exceeds the default cap."""
        calc = FineCalculator()
        fine = calc.apply_fine_cap(600.0)
        assert fine == 500.0
    
    def test_apply_fine_cap_custom_cap(self) -> None:
        """Test fine cap with custom cap value."""
        calc = FineCalculator()
        fine = calc.apply_fine_cap(200.0, cap=150.0)
        assert fine == 150.0
    
    def test_apply_fine_cap_negative_fine(self) -> None:
        """Test error handling for negative fine amount."""
        calc = FineCalculator()
        
        with pytest.raises(FineCalculationError):
            calc.apply_fine_cap(-50.0)
    
    def test_apply_fine_cap_negative_cap(self) -> None:
        """Test error handling for negative cap."""
        calc = FineCalculator()
        
        with pytest.raises(FineCalculationError):
            calc.apply_fine_cap(100.0, cap=-50.0)
    
    def test_calculate_fine_with_member_payload_valid(self) -> None:
        """Test fine calculation with member payload."""
        calc = FineCalculator(daily_fine_rate=50.0)
        member_payload = {'member_id': 'M1', 'name': 'John Doe'}
        
        fine = calc.calculate_fine_with_member_payload(member_payload, overdue_days=3)
        assert fine == 150.0
    
    def test_calculate_fine_with_member_payload_zero_days(self) -> None:
        """Test fine calculation with zero overdue days."""
        calc = FineCalculator()
        member_payload = {'member_id': 'M1'}
        
        fine = calc.calculate_fine_with_member_payload(member_payload, overdue_days=0)
        assert fine == 0.0
    
    def test_calculate_fine_with_member_payload_invalid_payload(self) -> None:
        """Test error handling for invalid member payload."""
        calc = FineCalculator()
        
        with pytest.raises(FineCalculationError):
            calc.calculate_fine_with_member_payload("not a dict", overdue_days=5)
    
    def test_calculate_fine_with_member_payload_missing_member_id(self) -> None:
        """Test error handling when member_id is missing."""
        calc = FineCalculator()
        member_payload = {'name': 'John'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_fine_with_member_payload(member_payload, overdue_days=5)
    
    def test_calculate_fine_with_member_payload_negative_days(self) -> None:
        """Test error handling for negative overdue days."""
        calc = FineCalculator()
        member_payload = {'member_id': 'M1'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_fine_with_member_payload(member_payload, overdue_days=-5)
    
    def test_calculate_fine_with_member_payload_non_integer_days(self) -> None:
        """Test error handling for non-integer overdue days."""
        calc = FineCalculator()
        member_payload = {'member_id': 'M1'}
        
        with pytest.raises(FineCalculationError):
            calc.calculate_fine_with_member_payload(member_payload, overdue_days=5.5)
