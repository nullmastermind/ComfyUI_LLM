# ComfyUI Custom Node Development Cheatsheet

## 1. Directory Structure
```
ComfyUI/custom_nodes/your_node_name/
├── __init__.py          # Node registration
├── your_node.py         # Node implementation
└── js/                  # Client-side code
    └── extension.js     # UI extensions
```

## 2. Basic Node Structure
```python
class CustomNode:
    CATEGORY = "my_category"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "main_method"
    OUTPUT_NODE = False  # True if node outputs final result
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "number": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "step": 1
                }),
                "choice": (["option1", "option2"], {"default": "option1"}),
                "model": ("MODEL",),
            },
            "optional": {
                "optional_param": ("FLOAT", {"default": 1.0})
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    def main_method(self, **kwargs):
        # Process inputs
        result = process_data(kwargs)
        return (result,)  # Always return a tuple
```

## 3. Node Registration (__init__.py)
```python
from .your_node import CustomNode

NODE_CLASS_MAPPINGS = {
    "My Custom Node": CustomNode
}

# Optional: Custom display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "My Custom Node": "Friendly Display Name"
}

# For client-side extensions
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
```

## 4. Advanced Node Features

### Validation
```python
@classmethod
def VALIDATE_INPUTS(cls, **kwargs):
    if invalid_condition:
        return "Error message"
    return True

@classmethod
def IS_CHANGED(cls, input_value):
    # Return float("NaN") to always trigger execution
    return hash(input_value)
```

### List Processing
```python
class ListNode:
    INPUT_IS_LIST = True   # Process inputs as lists
    OUTPUT_IS_LIST = True  # Return outputs as lists
```

### Lazy Evaluation
```python
@classmethod
def INPUT_TYPES(cls):
    return {
        "required": {
            "lazy_input": ("IMAGE", {"lazy": True})
        }
    }

def check_lazy_status(self, *args):
    # Return list of input names needed
    return ["input_name"]
```

## 5. Client-Side Extension (JavaScript)

### Basic Extension Setup
```javascript
import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
    name: "my.extension.name",
    async setup() {
        // Setup code
    },
    async init() {
        // Called after graph creation, before node registration
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Modify node behavior before registration
    },
    async nodeCreated(node) {
        // Called when node is created
    }
});
```

### Event Handling
```javascript
// Listen for server messages
api.addEventListener("my.message.type", (event) => {
    console.log(event.detail);
});

// Custom node click handling
if (node?.comfyClass === "My Node Name") {
    const original_onMouseDown = node.onMouseDown;
    node.onMouseDown = function(e, pos, canvas) {
        // Custom handling
        return original_onMouseDown?.apply(this, arguments);
    }
}
```

### Custom Menus
```javascript
// Add right-click menu options
nodeType.prototype.getExtraMenuOptions = function(_, options) {
    options.push({
        content: "Custom Action",
        callback: async () => {
            // Action code
        }
    });
}
```

## 6. Server-Client Communication

### Server Side (Python)
```python
from server import PromptServer

def node_method(self, **kwargs):
    # Send message to client
    PromptServer.instance.send_sync("my.message.type", {
        "node": kwargs["unique_id"],
        "data": some_data
    })
    return (result,)
```

### Client Side (JavaScript)
```javascript
// Handle server messages
api.addEventListener("my.message.type", (event) => {
    const { node, data } = event.detail;
    // Handle message
});
```

## 7. Settings and Preferences
```javascript
// Add user setting
app.ui.settings.addSetting({
    id: "my.setting.id",
    name: "Setting Name",
    type: "boolean",
    defaultValue: false,
    onChange: (newVal, oldVal) => {
        console.log("Setting changed:", newVal);
    }
});

// Read setting
const value = app.ui.settings.getSettingValue("my.setting.id", defaultValue);
```

Remember:
- Always restart ComfyUI after adding/modifying nodes
- Return tuples from node functions
- Use proper tensor shapes for image processing
- Test thoroughly before distribution
- Handle errors gracefully
- Document your code
- Consider compatibility with other custom nodes