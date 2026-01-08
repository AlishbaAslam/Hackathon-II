"""Unit tests for task alerts logic."""

import pytest
from datetime import datetime, timedelta
from src.todo_service import TodoService


def test_get_upcoming_alerts():
    service = TodoService()
    now = datetime.now()

    # Task due in 5 minutes
    due_5 = (now + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M").split()
    service.add_task(title="Due soon", due_date=due_5[0], due_time=due_5[1])

    # Task due in 30 minutes
    due_30 = (now + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M").split()
    service.add_task(title="Later", due_date=due_30[0], due_time=due_30[1])

    # Completed task
    due_2 = (now + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M").split()
    t_comp = service.add_task(title="Completed", due_date=due_2[0], due_time=due_2[1])
    service.toggle_complete(t_comp.id)

    # Overdue task (last minute)
    due_past = (now - timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M").split()
    service.add_task(title="Overdue", due_date=due_past[0], due_time=due_past[1])

    alerts = service.get_upcoming_alerts(window_minutes=15)

    assert len(alerts) == 2
    titles = [t.title for t in alerts]
    assert "Due soon" in titles
    assert "Overdue" in titles
    assert "Later" not in titles
    assert "Completed" not in titles
