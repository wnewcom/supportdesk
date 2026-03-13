# Run from bench: bench --site erp.local execute supportdesk.find_bad_module.find_bad_module
# Finds which app + module causes migrate to fail (get_module(...).__file__ is None).

def find_bad_module():
    import frappe
    bad = []
    for app in frappe.get_installed_apps():
        modules = frappe.local.app_modules.get(app) or []
        for mod in modules:
            modname = app + "." + mod
            try:
                m = frappe.get_module(modname)
                f = getattr(m, "__file__", None)
                if f is None:
                    bad.append((app, mod, modname))
                    print(f"BAD: app={app!r} module={mod!r} (__file__ is None)")
                else:
                    print(f"OK: {modname!r}")
            except Exception as e:
                bad.append((app, mod, str(e)))
                print(f"FAIL: app={app!r} module={mod!r} -> {e}")
    if bad:
        print("\nFix: In the app(s) above, set modules.txt and module folder to match (case-sensitive on Linux).")
    return bad
