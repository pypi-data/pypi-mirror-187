PocketCRM is a simple tool to allow you to build out and test your CRM progress. in future versions, we will have stages for Account management. for now we just have notes per account and to allow you track an output of customer accounts with relationship notes:)

Please consider using the BDevManager2 libary with PocketCRM. This way you can add quilifyed notes from calls with the BANT function to add Qulifyed notes to your PocketCRM. Integration coming soon to create a Sales Data Pipeline framework... for the SMB Community.  

To run, create a main.py file and add:

    from crm_eng import CRM, GUI

    gui = GUI()
    gui.root.mainloop()