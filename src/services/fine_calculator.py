"""Fine calculator service for managing overdue charges in the library system."""

from typing import Dict, Any, Optional
from datetime import datetime
from models.exceptions import FineCalculationError


class FineCalculator:
    """Service for calculating overdue fines based on member and book information."""
    
    DEFAULT_DAILY_FINE_RATE: float = 50.0
    MAX_FINE_CAP: float = 500.0
    
    def __init__(self, daily_fine_rate: float = DEFAULT_DAILY_FINE_RATE) -> None:
        """
        Initialize the FineCalculator with a daily fine rate.
        
        Args:
            daily_fine_rate: The amount charged per day of overdue (default: 50.0)
        
        Raises:
            FineCalculationError: If daily_fine_rate is not positive
        """
        if daily_fine_rate <= 0:
            raise FineCalculationError(
                f"Daily fine rate must be positive, got {daily_fine_rate}"
            )
        self.daily_fine_rate: float = daily_fine_rate
    
    def calculate_overdue_fine(
        self,
        due_date_payload: Dict[str, Any],
        return_date_payload: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate the overdue fine based on due date and return date.
        
        Args:
            due_date_payload: Dictionary containing 'date' key with ISO format date string
            return_date_payload: Optional dictionary containing 'date' key for return date.
                                 If None, uses current datetime.
        
        Returns:
            The calculated fine amount (non-negative)
        
        Raises:
            FineCalculationError: If dates are invalid or calculation fails
        """
        if not isinstance(due_date_payload, dict) or 'date' not in due_date_payload:
            raise FineCalculationError(
                "due_date_payload must be a dict with 'date' key"
            )
        
        try:
            due_date = datetime.fromisoformat(due_date_payload['date'])
        except (ValueError, TypeError) as e:
            raise FineCalculationError(
                f"Invalid due_date format: {due_date_payload['date']}"
            ) from e
        
        if return_date_payload is None:
            return_date = datetime.now()
        else:
            if not isinstance(return_date_payload, dict) or 'date' not in return_date_payload:
                raise FineCalculationError(
                    "return_date_payload must be a dict with 'date' key"
                )
            try:
                return_date = datetime.fromisoformat(return_date_payload['date'])
            except (ValueError, TypeError) as e:
                raise FineCalculationError(
                    f"Invalid return_date format: {return_date_payload['date']}"
                ) from e
        
        if return_date < due_date:
            return 0.0
        
        days_overdue = (return_date - due_date).days
        fine_amount = days_overdue * self.daily_fine_rate
        
        return fine_amount
    
    def calculate_member_total_fine(
        self,
        member_payload: Dict[str, Any],
        additional_charges: float = 0.0
    ) -> float:
        """
        Calculate total fine for a member including accumulated fines and additional charges.
        
        Args:
            member_payload: Dictionary containing member data with 'accumulated_fines' key
            additional_charges: Additional charges to add to the total (default: 0.0)
        
        Returns:
            Total fine amount for the member
        
        Raises:
            FineCalculationError: If member_payload is invalid or contains negative fines
        """
        if not isinstance(member_payload, dict):
            raise FineCalculationError("member_payload must be a dictionary")
        
        if 'accumulated_fines' not in member_payload:
            raise FineCalculationError(
                "member_payload must contain 'accumulated_fines' key"
            )
        
        accumulated_fines = member_payload['accumulated_fines']
        
        if not isinstance(accumulated_fines, (int, float)):
            raise FineCalculationError(
                f"accumulated_fines must be numeric, got {type(accumulated_fines).__name__}"
            )
        
        if accumulated_fines < 0:
            raise FineCalculationError(
                f"accumulated_fines cannot be negative, got {accumulated_fines}"
            )
        
        if additional_charges < 0:
            raise FineCalculationError(
                f"additional_charges cannot be negative, got {additional_charges}"
            )
        
        total_fine = accumulated_fines + additional_charges
        return total_fine
    
    def apply_fine_cap(self, fine_amount: float, cap: Optional[float] = None) -> float:
        """
        Apply a cap to the fine amount to prevent excessive charges.
        
        Args:
            fine_amount: The calculated fine amount
            cap: Maximum fine amount allowed (default: MAX_FINE_CAP)
        
        Returns:
            The capped fine amount
        
        Raises:
            FineCalculationError: If fine_amount or cap is negative
        """
        if fine_amount < 0:
            raise FineCalculationError(
                f"fine_amount cannot be negative, got {fine_amount}"
            )
        
        cap_limit = cap if cap is not None else self.MAX_FINE_CAP
        
        if cap_limit < 0:
            raise FineCalculationError(
                f"cap cannot be negative, got {cap_limit}"
            )
        
        return min(fine_amount, cap_limit)
    
    def calculate_fine_with_member_payload(
        self,
        member_payload: Dict[str, Any],
        overdue_days: int
    ) -> float:
        """
        Calculate fine amount for a member based on days overdue.
        
        Args:
            member_payload: Dictionary containing member data (for validation)
            overdue_days: Number of days the book is overdue
        
        Returns:
            Calculated fine amount
        
        Raises:
            FineCalculationError: If parameters are invalid
        """
        if not isinstance(member_payload, dict):
            raise FineCalculationError("member_payload must be a dictionary")
        
        if 'member_id' not in member_payload:
            raise FineCalculationError(
                "member_payload must contain 'member_id' key"
            )
        
        if not isinstance(overdue_days, int):
            raise FineCalculationError(
                f"overdue_days must be an integer, got {type(overdue_days).__name__}"
            )
        
        if overdue_days < 0:
            raise FineCalculationError(
                f"overdue_days cannot be negative, got {overdue_days}"
            )
        
        fine_amount = overdue_days * self.daily_fine_rate
        return fine_amount
