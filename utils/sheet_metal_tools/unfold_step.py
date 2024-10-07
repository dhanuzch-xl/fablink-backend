

def getUnfold(k_factor_lookup, solid, subelement, facename):
    resPart = None
    normalVect = None
    folds = None
    theName = None
    faceSel = ""
    ob_Name = solid.Name
    err_code = 0

    normalVect = subelement.normalAt(0, 0)
    FreeCAD.Console.PrintLog(f"name: {facename}\n ")
    f_number = int(facename.lstrip("Face")) - 1

    startzeit = time.process_time()

    TheTree = SheetTree(
        solid.Shape, f_number, k_factor_lookup
    )  # initializes the tree-structure
    if TheTree.error_code is None:
        TheTree.Bend_analysis(
            f_number, None
        )  # traverses the shape and builds the tree-structure
        endzeit = time.process_time()
        FreeCAD.Console.PrintLog("Analytical time: " + str(endzeit - startzeit) + "\n")

        if TheTree.error_code is None:
            # TheTree.showFaces()
            theFaceList, foldLines = TheTree.unfold_tree2(
                TheTree.root
            )  # traverses the tree-structure
            if TheTree.error_code is None:
                unfoldTime = time.process_time()
                FreeCAD.Console.PrintLog(
                    "time to run the unfold: " + str(unfoldTime - endzeit) + "\n"
                )
                folds = Part.Compound(foldLines)
                # Part.show(folds, 'Fold_Lines')
                try:
                    newShell = Part.Shell(theFaceList)
                except:
                    FreeCAD.Console.PrintLog(
                        "couldn't join some faces, show only single faces!\n"
                    )
                    resPart = Part.Compound(theFaceList)
                    # for newFace in theFaceList:
                    # Part.show(newFace)
                else:
                    try:
                        TheSolid = Part.Solid(newShell)
                        solidTime = time.process_time()
                        FreeCAD.Console.PrintLog(
                            "Time to make the solid: "
                            + str(solidTime - unfoldTime)
                            + "\n"
                        )
                    except:
                        FreeCAD.Console.PrintLog(
                            "Couldn't make a solid, show only a shell, Faces in List: "
                            + str(len(theFaceList))
                            + "\n"
                        )
                        resPart = newShell
                        # Part.show(newShell)
                        showTime = time.process_time()
                        FreeCAD.Console.PrintLog(
                            "Show time: " + str(showTime - unfoldTime) + "\n"
                        )
                    else:
                        try:
                            cleanSolid = TheSolid.removeSplitter()
                            # Part.show(cleanSolid)
                            resPart = cleanSolid

                        except:
                            # Part.show(TheSolid)
                            resPart = TheSolid
                        showTime = time.process_time()
                        FreeCAD.Console.PrintLog(
                            "Show time: "
                            + str(showTime - solidTime)
                            + " total time: "
                            + str(showTime - startzeit)
                            + "\n"
                        )

    if TheTree.error_code is not None:
        if TheTree.error_code == 1:
            FreeCAD.Console.PrintError(
                "Error at Face" + str(TheTree.failed_face_idx + 1) + "\n"
            )
            FreeCAD.Console.PrintError(
                "Trying to repeat the unfold process again with the Sewed copied Shape\n"
            )
            FreeCAD.ActiveDocument.openTransaction("sanitize")
            sew_Shape()
            FreeCAD.ActiveDocument.commitTransaction()
            ob = FreeCAD.ActiveDocument.ActiveObject
            ob_Name = ob.Name
            ob.Label = solid.Label + "_copy"
            faceSel = facename
            err_code = TheTree.error_code
        else:
            FreeCAD.Console.PrintError(
                "Error "
                + unfold_error[TheTree.error_code]
                + " at Face"
                + str(TheTree.failed_face_idx + 1)
                + "\n"
            )
    else:
        FreeCAD.Console.PrintLog("Unfold successful\n")

    endzeit = time.process_time()
    # FreeCAD.Console.PrintMessage("Analytical time: " + str(endzeit - startzeit) + "\n")
    return resPart, folds, normalVect, theName, err_code, faceSel, ob_Name

