import sys
import traceback

print("Testing imports...")
try:
    import backend.config as config
    print("backend.config imported")
    import backend.tools as tools
    print("backend.tools imported")
    import backend.prompts as prompts
    print("backend.prompts imported")
    # Verify format_query exists
    if not hasattr(prompts, 'format_query'):
        raise ImportError("format_query missing from prompts")
    print("prompts.format_query exists")
    
    import backend.agent as agent
    print("backend.agent imported")
    
    # app imports streamlit which might be slow or unhappy without a browser context, but let's try basic imports from it
    # actually, importing app might trigger st.set_page_config which fails.
    # So we just test the modules we touched.
    
    print("ALL IMPORTS SUCCESSFUL")
except Exception:
    traceback.print_exc()
