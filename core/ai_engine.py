PATHS = {
    "Python": [
        ("Programming fundamentals", "Learn variables, loops and functions."),
        ("Python OOP", "Practice classes and objects."),
        ("SQL basics", "Learn relational databases."),
        ("NumPy and Pandas", "Practice data analysis."),
        ("Build a Python project", "Create a portfolio project."),
    ],
    "Java": [
        ("Java fundamentals", "Learn syntax and control flow."),
        ("Object-oriented programming", "Practice classes and inheritance."),
        ("Data structures", "Study arrays, stacks and queues."),
        ("SQL and JDBC", "Connect Java to databases."),
        ("Build a Java project", "Create a portfolio application."),
    ],
    "Web Development": [
        ("HTML and CSS", "Build responsive web pages."),
        ("JavaScript", "Learn DOM and asynchronous basics."),
        ("Python and Django", "Build backend applications."),
        ("SQL", "Learn database design."),
        ("Deploy a project", "Publish your application."),
    ],
}

def recommend_next(skill, completed_titles):
    path = PATHS.get(skill, PATHS["Python"])
    done = {x.lower() for x in completed_titles}

    for title, description in path:
        if title.lower() not in done:
            return {
                "title": title,
                "description": description
            }

    return {
        "title": "Build an advanced portfolio project",
        "description": "Apply your skills in a larger project."
    }

def skill_gaps(skill, completed_titles):
    path = PATHS.get(skill, PATHS["Python"])
    done = {x.lower() for x in completed_titles}

    return [
        title for title, description in path
        if title.lower() not in done
    ]
