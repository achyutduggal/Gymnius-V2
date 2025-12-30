# app/domain/__init__.py
"""Domain layer - Core business logic, no external dependencies."""

from app.domain.entities import FoodItem, Meal, Macros, NutritionInfo

__all__ = ["FoodItem", "Meal", "Macros", "NutritionInfo"]