

if __name__=="__main__":
    # Hello
    modelOn = True
    app = QApplication(sys.argv)
    window = MainWindow(save = False)
    
    if modelOn:
        model = test(print_score = False)

        dockAssist = QDockWidget("Assistant", window)
        dockAssist.setMinimumSize(300, 100)
        window.addDockWidget(Qt.RightDockWidgetArea,dockAssist)

        dock = QDockWidget('Objectif ',window)
        dock.setMinimumSize(300, 100)
        window.addDockWidget(Qt.RightDockWidgetArea,dock)
        
        # Container
        container = QWidget()
        dock.setWidget(container)
        layout = QVBoxLayout(container)
        
        assistContainer = QWidget()
        dockAssist.setWidget(assistContainer)
        assistContaienrLayout = QVBoxLayout(assistContainer)
        
###########################     ASSISTANT     #################################
        
        #assist = AssistantGraph(model, window)
        assist = AssistantText(model, window)
        #assist = AssistantAlert(model, window)

###############################################################################

        # Help
        window.objectif = (window.helper.selected_obj, window.helper.angle)

        # Bouton reset
        button = QPushButton("Reset Assistant")
        button.clicked.connect(assist.reset)

        assistContaienrLayout.addWidget(button)
        assistContaienrLayout.addWidget(assist)
        layout.addWidget(window.helper)
        

    window.show()
    app.exec_()

