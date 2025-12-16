#include "scope_table.h"

class symbol_table
{
private:
    scope_table *current_scope;
    int bucket_count;
    int current_scope_id;

public:

    // Constructor
    symbol_table(int bucket_count)
    {
        this->bucket_count = bucket_count;
        this->current_scope_id = 1;
        current_scope = new scope_table(bucket_count, current_scope_id, NULL);
    }

    // Destructor
    ~symbol_table()
    {
        while (current_scope != NULL)
        {
            scope_table *temp = current_scope;
            current_scope = current_scope->get_parent_scope();
            delete temp;
        }
    }

    // Enter new scope
    void enter_scope()
    {
        current_scope_id++;
        scope_table *new_scope = new scope_table(bucket_count, current_scope_id, current_scope);
        current_scope = new_scope;
    }

    // Exit current scope
    void exit_scope()
    {
        if (current_scope == NULL)
            return;

        scope_table *parent = current_scope->get_parent_scope();

        delete current_scope;

        current_scope = parent;
    }

    // Insert symbol
    bool insert(symbol_info *symbol)
    {
        if (current_scope == NULL)
            return false;
        return current_scope->insert_in_scope(symbol);
    }

    // Lookup symbol in all scopes
    symbol_info *lookup(symbol_info *symbol)
    {
        scope_table *temp = current_scope;
        while (temp != NULL)
        {
            symbol_info *found = temp->lookup_in_scope(symbol);
            if (found != NULL)
            {
                return found;
            }
            temp = temp->get_parent_scope();
        }
        return NULL;
    }

    // Print current scope and all parent scopes
    void print_current_scope()
    {
        if (current_scope != NULL)
        {
            outlog << endl
                   << "################################" << endl
                   << endl;

            current_scope->print_scope_table(outlog);

            outlog << "################################" << endl
                   << endl;
        }
    }

    // Print all scopes
    void print_all_scopes(ofstream &outlog)
    {
        outlog << "Symbol Table" << endl
               << endl;
        outlog << "################################" << endl
               << endl;

        scope_table *temp = current_scope;
        while (temp != NULL)
        {
            temp->print_scope_table(outlog);
            temp = temp->get_parent_scope();
        }

        outlog << "################################" << endl;
    }

    // Get current scope ID
    int get_current_scope_id()
    {
        return current_scope_id;
    }

    // Check if in global scope
    bool is_global_scope()
    {
        return current_scope != NULL && current_scope->get_parent_scope() == NULL;
    }

    // Lookup only in current scope
    symbol_info *lookup_current_scope(symbol_info *symbol)
    {
        if (current_scope == NULL)
            return NULL;
        return current_scope->lookup_in_scope(symbol);
    }
};

// complete the methods of symbol_table class

// void symbol_table::print_all_scopes(ofstream& outlog)
// {
//     outlog<<"################################"<<endl<<endl;
//     scope_table *temp = current_scope;
//     while (temp != NULL)
//     {
//         temp->print_scope_table(outlog);
//         temp = temp->get_parent_scope();
//     }
//     outlog<<"################################"<<endl<<endl;
// }