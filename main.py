# import streamlit as st
# import json
# import copy

# st.set_page_config(page_title="MT5 Symbol Suffix Generator", layout="wide")
# st.title("MT5 Symbol Suffix Generator")

# # ===================== Helpers =====================
# def normalize_path(p):
#     return p.replace("/", "\\")

# # def apply_suffix(symbol, suffix):
# #     base = symbol.split(".", 1)[0]
# #     return f"{base}{suffix}"

# def apply_suffix(symbol, suffix, remove_existing=True):
#     """
#     Handles:
#     - Removing old suffix
#     - Adding suffix with dot
#     - Adding suffix without dot
#     - Pure removal (empty suffix)
#     """

#     if remove_existing:
#         base = symbol.split(".", 1)[0]
#     else:
#         base = symbol

#     # If suffix is empty → only remove
#     if not suffix:
#         return base

#     # If suffix starts with dot → append directly
#     if suffix.startswith("."):
#         return f"{base}{suffix}"

#     # If suffix does NOT start with dot → append directly without dot
#     return f"{base}{suffix}"

# def build_tree(symbols):
#     root = {}

#     for sym in symbols:
#         parts = normalize_path(sym["Path"]).split("\\")
#         folders = parts[:-1]  # exclude symbol itself

#         node = root
#         full_path = []

#         for f in folders:
#             full_path.append(f)
#             path = "\\".join(full_path)

#             if f not in node:
#                 node[f] = {
#                     "path": path,
#                     "children": {},
#                     "symbols": []
#                 }

#             node = node[f]["children"]

#         # attach symbol to leaf folder
#         leaf = root
#         for i, f in enumerate(folders):
#             leaf = leaf[f]
#             if i < len(folders) - 1:
#                 leaf = leaf["children"]

#         leaf["symbols"].append(sym)

#     return root

# def count_symbols(node):
#     total = len(node["symbols"])
#     for child in node["children"].values():
#         total += count_symbols(child)
#     return total

# # ===================== Tree Renderers =====================
# def render_tree_selectable(tree):
#     for name, node in tree.items():
#         chk_key = f"chk_{node['path']}"

#         if chk_key not in st.session_state:
#             st.session_state[chk_key] = False

#         total = count_symbols(node)

#         st.checkbox(
#             f"📁 {name} ({total})",
#             key=chk_key
#         )

#         with st.expander(name):
#             if node["children"]:
#                 render_tree_selectable(node["children"])
#             for s in node["symbols"]:
#                 st.write(f"📄 {s['Symbol']}")

# def render_tree_preview(tree):
#     for name, node in tree.items():
#         total = count_symbols(node)

#         with st.expander(f"📁 {name} ({total})"):
#             if node["children"]:
#                 render_tree_preview(node["children"])
#             for s in node["symbols"]:
#                 st.write(f"📄 {s['Symbol']}")

# # ===================== Upload =====================
# uploaded = st.file_uploader("Upload your .json file and get the new suffix symbols in few clicks", type=["json"])

# if uploaded:
#     data = json.load(uploaded)
#     symbols = data["Server"][0]["ConfigSymbols"]

#     tree = build_tree(symbols)

#     st.subheader("📁 Uploaded Symbol Structure")

#     select_all = st.checkbox("Select all folders")

#     if select_all:
#         def mark_all(tree):
#             for node in tree.values():
#                 st.session_state[f"chk_{node['path']}"] = True
#                 mark_all(node["children"])
#         mark_all(tree)

#     render_tree_selectable(tree)

#     st.divider()

#     # ===================== Inputs =====================
#     suffix = st.text_input("Enter suffix (example: .f, .pro)")
#     keep_source = st.radio("Keep source for history synchronization?", ["Yes", "No"])
#     new_root = st.text_input("New root folder name (example: Symbol.f)")
#     remove_existing = st.radio(
#         "Remove existing suffix before applying new one?",
#         ["Yes", "No"]
#     )

#     submit = st.button("Generate Symbols")

#     if submit:
#         # ---------- Validation ----------
#         # if not suffix.startswith("."):
#         #     st.error("Suffix must start with a dot (e.g. .f)")
#         #     st.stop()

#         if not new_root:
#             st.error("New root folder name is required.")
#             st.stop()

#         selected_paths = {
#             k.replace("chk_", "")
#             for k, v in st.session_state.items()
#             if k.startswith("chk_") and v
#         }

#         if not selected_paths:
#             st.error("No folders selected.")
#             st.stop()

#         # ---------- Generate ----------
#         new_symbols = []

#         for sym in symbols:
#             old_path = normalize_path(sym["Path"])
#             folder = "\\".join(old_path.split("\\")[:-1])

#             if folder not in selected_paths:
#                 continue

#             new_sym = copy.deepcopy(sym)
#             # new_symbol = apply_suffix(sym["Symbol"], suffix)

#             new_symbol = apply_suffix(
#                 sym["Symbol"],
#                 suffix.strip(),
#                 remove_existing == "Yes"
#             )

#             path_parts = old_path.split("\\")
#             path_parts[0] = new_root  # rename root folder

#             new_sym["Symbol"] = new_symbol
#             new_sym["Path"] = "\\".join(path_parts[:-1] + [new_symbol])
#             new_sym["Source"] = sym["Symbol"] if keep_source == "Yes" else ""


#             new_symbols.append(new_sym)

#         if not new_symbols:
#             st.error("No symbols generated.")
#             st.stop()

#         # ---------- Preview ----------
#         preview_tree = build_tree(new_symbols)

#         st.subheader("🔍 Preview Generated Symbols")
#         render_tree_preview(preview_tree)

#         # ---------- Export ----------
#         data["Server"][0]["ConfigSymbols"] = new_symbols

#         json_bytes = json.dumps(
#             data,
#             indent=4,
#             ensure_ascii=False
#         ).encode("utf-16")

#         st.success(f"Generated {len(new_symbols)} symbols successfully.")

#         st.download_button(
#             "Download MT5 Symbols JSON",
#             json_bytes,
#             file_name="symbols_generated.json",
#             mime="application/json"
#         )





#
# import streamlit as st
# import json
# import copy
#
# st.set_page_config(page_title="MT5 Symbol Suffix Generator", layout="wide")
# st.title("MT5 Symbol Suffix Generator")
#
# # ===================== Helpers =====================
# def normalize_path(p):
#     return p.replace("/", "\\")
#
# # def apply_suffix(symbol, suffix):
# #     base = symbol.split(".", 1)[0]
# #     return f"{base}{suffix}"
#
# def apply_suffix(symbol, suffix, remove_existing=True):
#     """
#     Handles:
#     - Removing old suffix
#     - Adding suffix with dot
#     - Adding suffix without dot
#     - Pure removal (empty suffix)
#     """
#
#     if remove_existing:
#         base = symbol.split(".", 1)[0]
#     else:
#         base = symbol
#
#     # If suffix is empty → only remove
#     if not suffix:
#         return base
#
#     # If suffix starts with dot → append directly
#     if suffix.startswith("."):
#         return f"{base}{suffix}"
#
#     # If suffix does NOT start with dot → append directly without dot
#     return f"{base}{suffix}"
#
# def build_tree(symbols):
#     root = {}
#
#     for sym in symbols:
#         parts = normalize_path(sym["Path"]).split("\\")
#         folders = parts[:-1]  # exclude symbol itself
#
#         node = root
#         full_path = []
#
#         for f in folders:
#             full_path.append(f)
#             path = "\\".join(full_path)
#
#             if f not in node:
#                 node[f] = {
#                     "path": path,
#                     "children": {},
#                     "symbols": []
#                 }
#
#             node = node[f]["children"]
#
#         # attach symbol to leaf folder
#         leaf = root
#         for i, f in enumerate(folders):
#             leaf = leaf[f]
#             if i < len(folders) - 1:
#                 leaf = leaf["children"]
#
#         leaf["symbols"].append(sym)
#
#     return root
#
# def count_symbols(node):
#     total = len(node["symbols"])
#     for child in node["children"].values():
#         total += count_symbols(child)
#     return total
#
# # ===================== Tree Renderers =====================
# def render_tree_selectable(tree):
#     for name, node in tree.items():
#         chk_key = f"chk_{node['path']}"
#
#         if chk_key not in st.session_state:
#             st.session_state[chk_key] = False
#
#         total = count_symbols(node)
#
#         st.checkbox(
#             f"📁 {name} ({total})",
#             key=chk_key
#         )
#
#         with st.expander(name):
#             if node["children"]:
#                 render_tree_selectable(node["children"])
#             for s in node["symbols"]:
#                 st.write(f"📄 {s['Symbol']}")
#
# def render_tree_preview(tree):
#     for name, node in tree.items():
#         total = count_symbols(node)
#
#         with st.expander(f"📁 {name} ({total})"):
#             if node["children"]:
#                 render_tree_preview(node["children"])
#             for s in node["symbols"]:
#                 st.write(f"📄 {s['Symbol']}")
#
# # ===================== Upload =====================
# uploaded = st.file_uploader("Upload your .json file and get the new suffix symbols in few clicks", type=["json"])
#
# if uploaded:
#     data = json.load(uploaded)
#     symbols = data["Server"][0]["ConfigSymbols"]
#
#     tree = build_tree(symbols)
#
#     st.subheader("📁 Uploaded Symbol Structure")
#
#     select_all = st.checkbox("Select all folders")
#
#     if select_all:
#         def mark_all(tree):
#             for node in tree.values():
#                 st.session_state[f"chk_{node['path']}"] = True
#                 mark_all(node["children"])
#         mark_all(tree)
#
#     render_tree_selectable(tree)
#
#     st.divider()
#
#     # ===================== Inputs =====================
#     suffix = st.text_input("Enter suffix (example: .f, .pro)")
#     keep_source = st.radio("Keep source for history synchronization?", ["Yes", "No"])
#     new_root = st.text_input("New root folder name (example: Symbol.f)")
#     remove_existing = st.radio(
#         "Remove existing suffix before applying new one?",
#         ["Yes", "No"]
#     )
#
#     submit = st.button("Generate Symbols")
#
#     if submit:
#         # ---------- Validation ----------
#         # if not suffix.startswith("."):
#         #     st.error("Suffix must start with a dot (e.g. .f)")
#         #     st.stop()
#
#         if not new_root:
#             st.error("New root folder name is required.")
#             st.stop()
#
#         selected_paths = {
#             k.replace("chk_", "")
#             for k, v in st.session_state.items()
#             if k.startswith("chk_") and v
#         }
#
#         if not selected_paths:
#             st.error("No folders selected.")
#             st.stop()
#
#         # ---------- Generate ----------
#         new_symbols = []
#
#         for sym in symbols:
#             old_path = normalize_path(sym["Path"])
#             folder = "\\".join(old_path.split("\\")[:-1])
#
#             if folder not in selected_paths:
#                 continue
#
#             new_sym = copy.deepcopy(sym)
#             # new_symbol = apply_suffix(sym["Symbol"], suffix)
#
#             new_symbol = apply_suffix(
#                 sym["Symbol"],
#                 suffix.strip(),
#                 remove_existing == "Yes"
#             )
#
#             path_parts = old_path.split("\\")
#             path_parts[0] = new_root  # rename root folder
#
#             new_sym["Symbol"] = new_symbol
#             new_sym["Path"] = "\\".join(path_parts[:-1] + [new_symbol])
#             new_sym["Source"] = sym["Symbol"] if keep_source == "Yes" else ""
#
#
#             new_symbols.append(new_sym)
#
#         if not new_symbols:
#             st.error("No symbols generated.")
#             st.stop()
#
#         # ---------- Preview ----------
#         preview_tree = build_tree(new_symbols)
#
#         st.subheader("🔍 Preview Generated Symbols")
#         render_tree_preview(preview_tree)
#
#         # ---------- Export ----------
#         data["Server"][0]["ConfigSymbols"] = new_symbols
#
#         json_bytes = json.dumps(
#             data,
#             indent=4,
#             ensure_ascii=False
#         ).encode("utf-16")
#
#         st.success(f"Generated {len(new_symbols)} symbols successfully.")
#
#         st.download_button(
#             "Download MT5 Symbols JSON",
#             json_bytes,
#             file_name="symbols_generated.json",
#             mime="application/json"
#         )
#
#
#

import streamlit as st
import json
import copy

st.set_page_config(page_title="MT5 Symbol Suffix Generator", layout="wide")
st.title("MT5 Symbol Suffix Generator")

# ===================== Helpers =====================

def normalize_path(p):
    return p.replace("/", "\\")


def apply_suffix(symbol, suffix, remove_existing=True):
    """
    Handles:
    - Removing old suffix
    - Adding suffix with dot
    - Adding suffix without dot
    - Pure removal (empty suffix)
    """

    if remove_existing:
        base = symbol.split(".", 1)[0]
    else:
        base = symbol

    # If suffix is empty → only remove
    if not suffix:
        return base

    # If suffix starts with dot → append directly
    if suffix.startswith("."):
        return f"{base}{suffix}"

    # If suffix does NOT start with dot → append directly without dot
    return f"{base}{suffix}"


def generate_source_symbol(symbol, source_suffix, remove_existing=True):
    """
    Generates source symbol with custom suffix

    Example:
    XAUUSD.p + .k => XAUUSD.k
    """

    if remove_existing:
        base = symbol.split(".", 1)[0]
    else:
        base = symbol

    if not source_suffix:
        return base

    if source_suffix.startswith("."):
        return f"{base}{source_suffix}"

    return f"{base}{source_suffix}"


def build_tree(symbols):
    root = {}

    for sym in symbols:

        parts = normalize_path(sym["Path"]).split("\\")
        folders = parts[:-1]

        node = root
        full_path = []

        for f in folders:

            full_path.append(f)
            path = "\\".join(full_path)

            if f not in node:
                node[f] = {
                    "path": path,
                    "children": {},
                    "symbols": []
                }

            node = node[f]["children"]

        # attach symbol to leaf folder
        leaf = root

        for i, f in enumerate(folders):

            leaf = leaf[f]

            if i < len(folders) - 1:
                leaf = leaf["children"]

        leaf["symbols"].append(sym)

    return root


def count_symbols(node):

    total = len(node["symbols"])

    for child in node["children"].values():
        total += count_symbols(child)

    return total


# ===================== Tree Renderers =====================

def render_tree_selectable(tree):

    for name, node in tree.items():

        chk_key = f"chk_{node['path']}"
        rename_key = f"rename_{node['path']}"

        if chk_key not in st.session_state:
            st.session_state[chk_key] = False

        if rename_key not in st.session_state:
            st.session_state[rename_key] = name

        total = count_symbols(node)

        # ================= Folder Row =================

        col1, col2 = st.columns([1, 2])

        with col1:
            st.checkbox(
                f"📁 {name} ({total})",
                key=chk_key
            )

        with col2:
            st.text_input(
                "Rename Folder",
                key=rename_key,
                label_visibility="collapsed"
            )

        # ================= Children =================

        with st.expander(f"Open {name}"):

            if node["children"]:
                render_tree_selectable(node["children"])

            for s in node["symbols"]:
                st.write(f"📄 {s['Symbol']}")


def render_tree_preview(tree):

    for name, node in tree.items():

        total = count_symbols(node)

        with st.expander(f"📁 {name} ({total})"):

            if node["children"]:
                render_tree_preview(node["children"])

            for s in node["symbols"]:
                st.write(f"📄 {s['Symbol']}")


# ===================== Upload =====================

uploaded = st.file_uploader(
    "Upload your .json file and get the new suffix symbols in few clicks",
    type=["json"]
)

if uploaded:

    data = json.load(uploaded)

    symbols = data["Server"][0]["ConfigSymbols"]

    tree = build_tree(symbols)

    st.subheader("📁 Uploaded Symbol Structure")

    select_all = st.checkbox("Select all folders")

    if select_all:

        def mark_all(tree):

            for node in tree.values():

                st.session_state[f"chk_{node['path']}"] = True

                mark_all(node["children"])

        mark_all(tree)

    render_tree_selectable(tree)

    st.divider()

    # ===================== Inputs =====================

    st.subheader("⚙️ Symbol Generation Settings")

    suffix = st.text_input(
        "Enter new symbol suffix",
        placeholder=".f / .pro / .ecn"
    )

    remove_existing = st.radio(
        "Remove existing suffix before applying new one?",
        ["Yes", "No"]
    )

    keep_source = st.radio(
        "Keep source for history synchronization?",
        ["Yes", "No"]
    )

    source_suffix = st.text_input(
        "Source symbol suffix (optional)",
        placeholder=".k / .raw / .main",
        help="Leave empty to only remove old suffix"
    )

    source_remove_existing = st.radio(
        "Remove existing suffix from source symbol?",
        ["Yes", "No"],
        key="src_remove"
    )

    new_root = st.text_input(
        "New root folder name",
        placeholder="Symbols.f"
    )

    st.divider()

    # ===================== Generate =====================

    submit = st.button("Generate Symbols")

    if submit:

        # ===================== Validation =====================

        if not new_root:
            st.error("New root folder name is required.")
            st.stop()

        selected_paths = {
            k.replace("chk_", "")
            for k, v in st.session_state.items()
            if k.startswith("chk_") and v
        }

        if not selected_paths:
            st.error("No folders selected.")
            st.stop()

        # ===================== Generate Symbols =====================

        new_symbols = []

        for sym in symbols:

            old_path = normalize_path(sym["Path"])

            folder = "\\".join(old_path.split("\\")[:-1])

            # Recursive selection support
            if not any(folder.startswith(p) for p in selected_paths):
                continue

            new_sym = copy.deepcopy(sym)

            # ===================== Generate New Symbol =====================

            new_symbol = apply_suffix(
                sym["Symbol"],
                suffix.strip(),
                remove_existing == "Yes"
            )

            # ===================== Update Path =====================

            path_parts = old_path.split("\\")

            # Rename folders directly from UI
            current_path = []

            for i in range(len(path_parts) - 1):

                current_path.append(path_parts[i])

                full_path = "\\".join(current_path)

                rename_key = f"rename_{full_path}"

                if rename_key in st.session_state:
                    path_parts[i] = st.session_state[rename_key]

            # Override root folder
            path_parts[0] = new_root

            # ===================== Assign New Symbol =====================

            new_sym["Symbol"] = new_symbol

            new_sym["Path"] = "\\".join(
                path_parts[:-1] + [new_symbol]
            )

            # ===================== Source Logic =====================

            if keep_source == "Yes":

                new_source = generate_source_symbol(
                    sym["Symbol"],
                    source_suffix.strip(),
                    source_remove_existing == "Yes"
                )

                new_sym["Source"] = new_source

            else:
                new_sym["Source"] = ""

            new_symbols.append(new_sym)

        # ===================== Validation =====================

        if not new_symbols:
            st.error("No symbols generated.")
            st.stop()

        # ===================== Preview =====================

        preview_tree = build_tree(new_symbols)

        st.subheader("🔍 Preview Generated Symbols")

        render_tree_preview(preview_tree)

        # ===================== Export =====================

        data["Server"][0]["ConfigSymbols"] = new_symbols

        json_bytes = json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ).encode("utf-16")

        st.success(
            f"Generated {len(new_symbols)} symbols successfully."
        )

        st.download_button(
            "Download MT5 Symbols JSON",
            json_bytes,
            file_name="symbols_generated.json",
            mime="application/json"
        )
