import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: 'CmcLLM.GraphArrange',
  setup(app) {
    const originalGetCanvasMenuOptions = LGraphCanvas.prototype.getCanvasMenuOptions
    LGraphCanvas.prototype.getCanvasMenuOptions = function() {
      const menuOptions = originalGetCanvasMenuOptions.call(this)

      menuOptions.push({
        content: '🧩 Organize nodes',
        callback: () => {
          const arrangeGraphNodes = function() {
            // Configuration
            const nodeSpacing = 32
            const excludedNodeTypes = new Set(['Note'])
            const imageNodeTypes = ['SaveImage', 'PreviewImage']

            // Get nodes in execution order
            const graphNodes = this.computeExecutionOrder(false, true).filter(
              node => !excludedNodeTypes.has(node.type)
            )
            const nodeColumns = []

            // Calculate node levels based on connections
            for (let i = graphNodes.length - 1; i >= 0; i--) {
              const currentNode = graphNodes[i]
              let maxLevel = null

              for (const output of currentNode.outputs || []) {
                if (output.links) {
                  for (const linkId of output.links) {
                    const targetNode = app.graph.getNodeById(
                      app.graph.links[linkId].target_id
                    )
                    if (!targetNode) continue

                    const targetLevel = targetNode._level - 1
                    if (maxLevel === null) maxLevel = targetLevel
                    else if (targetLevel < maxLevel) maxLevel = targetLevel
                  }
                }
              }
              if (maxLevel != null) currentNode._level = maxLevel
            }

            // Group nodes into columns
            for (let i = 0; i < graphNodes.length; ++i) {
              const currentNode = graphNodes[i]
              const columnIndex = currentNode._level || 1
              if (!nodeColumns[columnIndex]) {
                nodeColumns[columnIndex] = []
              }
              nodeColumns[columnIndex].push(currentNode)
            }

            // Position nodes in columns
            let horizontalPosition = nodeSpacing

            for (let columnIndex = 0; columnIndex < nodeColumns.length; ++columnIndex) {
              const currentColumn = nodeColumns[columnIndex]
              if (!currentColumn) continue

              // Sort nodes within column
              currentColumn.sort((nodeA, nodeB) => {
                let sortResult =
                  Number(!imageNodeTypes.includes(nodeA.type)) -
                  Number(!imageNodeTypes.includes(nodeB.type))

                if (sortResult === 0) {
                  sortResult =
                    (nodeA.inputs?.length || 0) - (nodeB.inputs?.length || 0)
                }

                if (sortResult === 0) {
                  sortResult =
                    (nodeA.outputs?.length || 0) - (nodeB.outputs?.length || 0)
                }

                return sortResult
              })

              // Layout nodes vertically
              let verticalPosition = nodeSpacing + LiteGraph.NODE_TITLE_HEIGHT
              let maxColumnWidth = 100

              for (let nodeIndex = 0; nodeIndex < currentColumn.length; ++nodeIndex) {
                const currentNode = currentColumn[nodeIndex]
                currentNode.pos[0] = horizontalPosition
                currentNode.pos[1] = verticalPosition

                if (currentNode.size[0] > maxColumnWidth) {
                  maxColumnWidth = currentNode.size[0]
                }

                verticalPosition +=
                  currentNode.size[1] +
                  nodeSpacing +
                  LiteGraph.NODE_TITLE_HEIGHT +
                  nodeIndex
              }

              // Right align nodes in column
              for (let nodeIndex = 0; nodeIndex < currentColumn.length; ++nodeIndex) {
                const currentNode = currentColumn[nodeIndex]
                currentNode.pos[0] += maxColumnWidth - currentNode.size[0]
              }

              horizontalPosition += maxColumnWidth + nodeSpacing
            }

            this.setDirtyCanvas(true, true)
          }
          // Apply
          arrangeGraphNodes.apply(app.graph)
        }
      })

      return menuOptions
    }
  }
})