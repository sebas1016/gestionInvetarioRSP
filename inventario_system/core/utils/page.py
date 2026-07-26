def page_context(
    *,
    title,
    description="",
    breadcrumbs=None,
    action=None,
    **kwargs,
):
    context = {
        "page_title": title,
        "page_description": description,
        "breadcrumbs": breadcrumbs or [],
        "page_action": action,
    }

    context.update(kwargs)

    return context