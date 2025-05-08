"""GraphQL queries used by the Mythic MCP tools."""

GET_LOADED_COMMANDS = """
subscription GetLoadedCommandsSubscription($callback_id: Int!){  
    loadedcommands(where: {callback_id: {_eq: $callback_id}}){  
        id  
        command {  
            cmd  
            id  
            attributes  
            payloadtype {  
                name  
                id  
            }  
            commandparameters {  
                id  
                parameter_type: type   
                choices  
                dynamic_query_function  
                required  
                name  
                ui_position  
                parameter_group_name  
                cli_name  
                display_name  
            }  
        }  
    }  
}
"""