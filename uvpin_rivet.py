import maya.api.OpenMaya as om

uvpin = cmds.createNode("uvPin")
cmds.connectAttr("pSphere1.worldMesh[0]", uvpin + ".deformedGeometry")

vertex = "pSphere1.vtx[279]"
cmds.select(vertex)
cmds.ConvertSelectionToUVs()
# get uv values
uv = cmds.polyEditUV(query = True)

# set UV coordinate for uv pin
cmds.setAttr(uvpin + ".coordinate[0].coordinateU", uv[0])
cmds.setAttr(uvpin + ".coordinate[0].coordinateV", uv[1])

decompose_matrix = cmds.createNode("decomposeMatrix")
compose_matrix = cmds.createNode("composeMatrix")
cmds.connectAttr("uvPin1.outputMatrix[0]", decompose_matrix + ".inputMatrix")
cmds.connectAttr(decompose_matrix + ".outputTranslate", compose_matrix + ".inputTranslate")
cmds.connectAttr(compose_matrix + ".outputMatrix", "control.offsetParentMatrix")

target_ctrl_world_matrix = cmds.getAttr("control.worldMatrix[0]")
parent_ctrl_inv_world_matrix = cmds.getAttr("sub_control.worldInverseMatrix[0]")

matrix1 = om.MMatrix(target_ctrl_world_matrix)
matrix2 = om.MMatrix(parent_ctrl_inv_world_matrix)
offset_matrix = matrix1 * matrix2

mult_matrix = cmds.createNode("multMatrix")
cmds.setAttr(mult_matrix + ".matrixIn[0]", offset_matrix, type = "matrix")
cmds.connectAttr("sub_control.worldMatrix[0]", mult_matrix + ".matrixIn[1]")
decompose_matrix2 = cmds.createNode("decomposeMatrix")
cmds.connectAttr(mult_matrix + ".matrixSum", decompose_matrix2 + ".inputMatrix")
cmds.connectAttr(decompose_matrix2 + ".outputRotate", compose_matrix + ".inputRotate")
