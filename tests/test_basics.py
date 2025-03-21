"""Basic tests for Lilith-Shell functionality."""
import os
import sys
import subprocess
import pytest
from unittest.mock import patch, MagicMock
from lilith_shell.executor import handle_call_tool

# Add necessary path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def mock_subprocess():
    """Mock subprocess.run to avoid executing actual commands."""
    with patch("subprocess.run") as mock_run:
        # Setup mock return value
        mock_process = MagicMock()
        mock_process.stdout = "test output"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        yield mock_run


@pytest.mark.asyncio
async def test_execute_simple_command(mock_subprocess):
    """Test basic command execution functionality."""
    # Arrange - mock_subprocess fixture takes care of it

    # Act
    result = await handle_call_tool(
        "execute_command", {"command": "echo test", "directory": "~"}
    )

    # Assert
    assert len(result) == 1
    assert "test output" in result[0].text
    assert "Exit code: 0" in result[0].text
    # Verify subprocess.run was called with expected parameters
    mock_subprocess.assert_called_once()
    args, kwargs = mock_subprocess.call_args
    assert kwargs["shell"] is True
    assert kwargs["args"] == "echo test"  # Changed from 'command' to 'args'
    assert os.path.expanduser("~") in kwargs["cwd"]


@pytest.mark.asyncio
async def test_command_with_error(mock_subprocess):
    """Test command execution with error."""
    # Arrange
    mock_subprocess.return_value.returncode = 1
    mock_subprocess.return_value.stderr = "error message"

    # Act
    result = await handle_call_tool(
        "execute_command", {"command": "invalid_command", "directory": "~"}
    )

    # Assert
    assert len(result) == 1
    assert "error message" in result[0].text
    assert "Exit code: 1" in result[0].text


@pytest.mark.asyncio
async def test_handle_invalid_tool():
    """Test handler rejects invalid tool names."""
    # Act & Assert
    with pytest.raises(ValueError, match="Unknown tool"):
        await handle_call_tool("invalid_tool", {})


@pytest.mark.asyncio
async def test_handle_missing_arguments():
    """Test handler requires arguments."""
    # Act & Assert
    with pytest.raises(ValueError, match="Missing arguments"):
        await handle_call_tool("execute_command", None)


@pytest.mark.asyncio
async def test_command_timeout(mock_subprocess):
    """Test command timeout handling."""
    # Arrange - set up subprocess.TimeoutExpired exception
    mock_subprocess.side_effect = subprocess.TimeoutExpired(
        cmd="sleep 999", timeout=300
    )

    # Act
    result = await handle_call_tool(
        "execute_command", {"command": "sleep 999", "directory": "~"}
    )

    # Assert
    assert len(result) == 1
    assert "timed out" in result[0].text.lower()
