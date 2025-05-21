from project_manager.app import get_all_tasks, add_task # Functions to test directly

def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"No tasks yet." in rv.data # From index.html when no tasks

def test_add_task_directly(app):
    """Test adding a task directly via the function and db."""
    with app.app_context(): # Need app context to use get_db()
        add_task("Test Title Direct", "Test Desc Direct")
        tasks = get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Test Title Direct"

def test_add_task_route(client):
    """Test adding a task via the /add route."""
    # First, check the page loads
    rv = client.get("/add")
    assert rv.status_code == 200

    # Then, post a new task
    rv = client.post("/add", data={"title": "Test Task Route", "description": "Test Desc Route"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Test Task Route" in rv.data # Check if it appears on the index page
    assert b"No tasks yet." not in rv.data

    # Verify it's in the database via direct function call if possible or by checking UI thoroughly
    # For simplicity here, we rely on the redirected page content

def test_index_route(client):
    """Test the index route loads."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<h1>Tasks</h1>" in rv.data # Check for a known element on the page

def test_init_db_command(runner):
    """Test the init-db command."""
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output
    # You could add more assertions here, e.g., check if the db file exists or a table exists
