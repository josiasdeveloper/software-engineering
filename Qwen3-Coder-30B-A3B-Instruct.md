STRATEGY 1: Identificação via Interface Base + Implementações Concretas

Questões para o modelo

"Estas duas classes implementam qual padrão de projeto em relação à interface abstrata anterior?"

"Como o cliente pode trocar entre estas implementações sem modificar seu código?" 

The two classes AnthropicLlmService and OpenAILlmService, which implement the abstract interface LlmService, exemplify the Strategy design pattern. This pattern allows you to encapsulate different algorithms or alternative behaviors within separate classes, allowing you to dynamically choose which strategy to use based on conditions or configurations. In this case, each class implements the same interface with specific behaviors for different LLM providers – one for Anthropic and another for OpenAI.

The advantage of this pattern is that the client can switch between implementations without needing to modify their code. This is possible because all clients access the service through the same abstract interface LlmService. When you need to change providers, for example, from Anthropic to OpenAI, you simply instantiate a different class, maintaining the same method calls. You can create a factory function that returns the appropriate implementation based on parameters, or use dependency injection to pass the desired implementation, making the client completely independent of the concrete implementation being used. Therefore, the business logic does not need to be altered when switching between different LLM providers, making the system more flexible and easier to maintain.


STRATEGY 2: Identificação via UserResolver (Autenticação)

1. "Qual padrão permite trocar entre diferentes métodos de autenticação (cookie vs JWT) sem modificar o Agent?"
2. "Como este padrão facilita a integração com sistemas de autenticação existentes?"

The Strategy pattern, which allows switching between different authentication methods (cookie vs. JWT) without modifying the Agent, is applied in the authentication architecture where the UserResolver interface defines a common contract for all user resolution strategies, while concrete implementations such as SimpleUserResolver, CookieUserResolver, and MyUserResolver encapsulate different specific authentication logics.

The Strategy pattern facilitates integration with existing authentication systems because it allows different authentication providers to be plugged into the same point in the system without altering the main agent code. The Agent receives a UserResolver instance during its initialization, and any implementation that follows the UserResolver interface can be used. This means that if you already have a JWT-based authentication system in production, you can create a MyUserResolver implementation that uses exactly your own token decoding and user data retrieval logic, without affecting any other part of the agent code. Similarly, if you are integrating with FastAPI or another framework that uses cookies, you can easily use CookieUserResolver. The Strategy pattern allows each strategy to implement its own authentication logic independently, maintaining a consistent interface and enabling transparent switching between different authentication mechanisms as needed.


STRATEGY 3: Identificação via WorkflowHandler

"Como o WorkflowHandler implementa o Strategy Pattern?"
"Que benefício há em poder trocar entre DefaultWorkflowHandler e CommandWorkflow?"


The WorkflowHandler implements the Strategy Pattern by defining an abstract interface that allows different workflow handling strategies before processing by the LLM. The abstract class WorkflowHandler establishes the contract with methods such as try_handle and get_starter_ui, while concrete implementations such as DefaultWorkflowHandler and CommandWorkflow provide specific behaviors. The agent depends only on the abstract interface, allowing different implementations to be injected as needed, following the principle of programming to interfaces and not to implementations.

The benefit of being able to switch between DefaultWorkflowHandler and CommandWorkflow is considerable: with DefaultWorkflowHandler, the agent follows the default behavior of always forwarding messages to the LLM, which is useful for basic scenarios or when no special handling is needed. With CommandWorkflow, it is possible to create custom logic that intercepts specific messages (such as commands starting with "/help" or "/report"), processes them directly without needing to send them to the LLM, and even provides custom interface components. This allows adding functionalities such as interface commands, quick shortcuts, or special message handling without modifying the agent's core, keeping the system flexible and extensible. The pattern facilitates the implementation of different workflow handling policies, allowing different environments or requirements to be met with distinct strategies, all without impacting the main agent code.


2. Template Method Pattern

STRATEGY 1: Identificação via Tool Base Class

Quais passos ele define e quais delega para subclasses?"

The get_schema() method in this class acts as a Template Method.

The steps it defines are:
1. Obtaining the argument schema - calls self.get_args_schema() to obtain the specific Pydantic model
2. Generating the JSON schema - checks if the model has model_json_schema() and extracts the corresponding schema
3. Building the final ToolSchema - assembles the ToolSchema object with name, description, parameters, and access groups

The steps it delegates to subclasses are:
- self.get_args_schema() - delegates to subclasses to provide the specific Pydantic argument model
- self.name` and self.description - delegates to subclasses to define the specific name and description values
- self.access_groups - delegates to subclasses to determine which groups have access (although it has a default implementation, it can be overridden)
This Template Method defines the fixed structure of the schema generation algorithm, but allows that Subclasses implement the specific aspects of each tool in the methods that are delegated, thus maintaining consistency in the format of the final result.


Snippet 1.2: Implementação Concreta (RunSqlTool)

"Como RunSqlTool implementa o Template Method definido na classe Tool?"
"Que método da classe base Tool usa os métodos abstratos implementados por RunSqlTool?"

RunSqlTool implements the Template Method defined in the Tool class through the implementation of abstract methods that are delegated by the get_schema() method. Specifically, RunSqlTool provides implementations for:

1. name - property that returns "run_sql"
2. description - property that returns the tool description
3. get_args_schema() - method that returns the RunSqlToolArgs type

When the get_schema() method of the base class Tool is called, it uses these methods implemented by RunSqlTool to build the complete schema that will be sent to the LLM.

The method of the base class Tool that uses the abstract methods implemented by RunSqlTool is precisely get_schema(). This method invokes:
- self.name (implemented by RunSqlTool)
- self.description (implemented by RunSqlTool)
- self.get_args_schema() (implemented by RunSqlTool)
In addition, RunSqlTool also implements the execute() method of the base class, which is another abstract method that defines the specific execution behavior of the tool. Therefore, RunSqlTool fully implements all abstract methods defined in the base class Tool, allowing the Template Method get_schema() to function correctly by having access to all the information needed to generate the complete schema for the LLM.


Snippet 1.3: Como o Template Method é Usado

"Como o ToolRegistry usa o Template Method get_schema() sem precisar conhecer os detalhes de cada ferramenta específica?"

The ToolRegistry uses the Template Method get_schema() generically because all the tool objects it manipulates follow a common interface that defines this method, but each implements its own specific logic to return the schema. When the registry calls tool.get_schema(), it doesn't need to know how each tool constructs its specific schema—it only knows that each one has this method and that it returns a ToolSchema object. This mechanism works through polymorphism: although the implementations may vary between tools (for example, a MySQL tool might collect schemas from a MySQL database and another might do it with PostgreSQL), the way the registry interacts with them is always the same. This allows the registry code to be much simpler and more reusable, since it doesn't need to be modified when new tools are added, as long as these new tools also implement the get_schema() method correctly. Thus, the Template Method allows the registry to obtain information about all schemas consistently, without needing to know the internal details of each implementation.


3. Abstract Factory Pattern

STRATEGY 1: Identificação via Component Creation

Snippet 1.1: Estrutura Base de Componentes

The from_records method acts as a Factory Method because it serves as a class method that instantiates and returns objects of the class itself (DataFrameComponent) in an encapsulated and standardized way. Instead of requiring users to manually create an instance of DataFrameComponent with all the parameters, the from_records method provides a more convenient and intuitive interface for creating instances based on structured data.

The family of objects it creates is the DataFrameComponent - a subclass of RichComponent that represents specific interface components for displaying tabular data. The from_records method is especially useful because it:

1. Automates metadata extraction - automatically retrieves column names from the first record
2. Automatically populates derived fields - calculates row and column counts, column types (optionally)
3. Facilitates building with real data - allows creating components directly from dictionary lists, which is a natural format for tabular data
4. Maintains consistency - ensures that all created components have the correct structure and necessary fields

This approach follows the Factory Method pattern because it encapsulates the complex logic of creating a DataFrame component, offering a simple interface for clients who need to create this specific type of UI component, without exposing the internal details of the object's creation.

4. Adapter Pattern

The LegacyVannaAdapter implements the Adapter Pattern by acting as an adapter that converts the interface of a legacy class (VannaBase) to the interface expected by the modern system (AgentMemory).

The adapter functions as an adaptation layer that allows modern code to use a different interface than the legacy implementation. It implements the AgentMemory interface (target interface) and contains an instance of VannaBase (legacy class).

In the save_tool_usage and search_similar_usage methods, the adapter converts calls from the new interface to existing methods of the legacy class, performing protocol translation. For example, it transforms a save_tool_usage call into an add_question_sql call from the legacy class, and converts results from get_similar_question_sql to the format expected by the new system.

Furthermore, the adapter inherits from ToolRegistry as well, demonstrating how the pattern can be combined with other patterns to create a more complete solution. The advantage is that modern code can use the new AgentMemory interface without needing to know it's interacting with a legacy system, maintaining compatibility and allowing existing methods to continue working while introducing new features. The pattern allows legacy systems to be integrated with new systems without major modifications to the client code.


5. Decorator/Chain of Responsibility

STRATEGY 1: Identificação via LlmMiddleware Chain

Snippet 1.1: Interface LlmMiddleware

The LlmMiddleware interface implements the Chain of Responsibility design pattern. This pattern allows multiple middleware instances to be chained together, where each middleware can process a request before sending it to the next, and process a response after receiving it from the next.

The interface defines two methods: before_llm_request and after_llm_response, which are called at different points in the lifecycle of a request to the LLM. When multiple instances are chained together, each can modify the request or response as needed, and the next instance in the chain receives the modified version of the request or the previously processed response. Chaining is usually implemented in a list or queue, where each middleware is executed sequentially, passing the processed result to the next middleware in the chain until the request reaches the final LLM or until the response returns completely through the chain. Thus, the pattern allows for the composition of complex behaviors in a modular and extensible way, without each middleware needing to know all the others.


Snippet 1.2: Chain Processing no Agent

The Agent clearly implements the Chain of Responsibility pattern through the use of middlewares. In the _send_llm_request method, it iterates through the self.llm_middlewares list in two steps: first applying all middlewares to the before_llm_request flow and then to the after_llm_response flow. Each middleware receives the request or response object, and can modify it before passing it to the next in the chain, as shown in the lines request = await middleware.before_llm_request(request) and response = await middleware.after_llm_response(request, response).
This implementation characterizes the Chain of Responsibility, not the Decorator. In the Chain of Responsibility, multiple handlers (middlewares) are executed sequentially, each processing the object and passing it on. In the Decorator model, there is a single chain of stacked objects, where each decorator adds new responsibilities to a central object through composition. The essential difference is that, in the Agent model, all middlewares are executed sequentially as part of the processing flow, and not as layers that decorate a single object—which confirms the application of the Chain of Responsibility principle.

STRATEGY 2: Identificação via LifecycleHook Chain

Snippet 2.1: Interface LifecycleHook

Os LifecycleHooks formam uma Chain of Responsibility executando-se sequencialmente na lista de hooks do agente. O código percorre todos os hooks em self.lifecycle_hooks e chama before_message em cada um. Se um hook retornar uma mensagem modificada (não None), essa mensagem é passada para o próximo hook através da variável modified_message. Isso permite que hooks subsequentes processem a mensagem já modificada pelo hook anterior, criando uma sequência de transformações que se acumulam. Cada hook tem a oportunidade de processar e alterar o estado (mensagem) que é passado adiante, caracterizando uma cadeia de processamento onde cada elemento pode modificar a entrada para o próximo.

Snippet 2.2: Chain Processing de Hooks

Lifecycle Hooks form a Chain of Responsibility because each hook is executed sequentially in the agent's hook list, where each one can modify the message for the next. In the code, the variable modified_message is initialized with the original message, and for each hook in the self.lifecycle_hooks list, if the hook returns a non-None value (indicating modification), that value replaces modified_message. This modified message is then passed to the next hook in the chain through the `modified_message variable. Thus, each hook has the opportunity to transform the message before it is processed by the agent, creating a sequence of chained modifications. The process continues until all hooks have been executed, with the final message being used for agent processing.

6. Observer Pattern

STRATEGY 1: Identificação via ObservabilityProvider

Snippet 1.1: Interface Observer (ObservabilityProvider)

The ObservabilityProvider acts as an Observer because it is an abstract interface that defines how observers should behave when receiving event notifications. It observes various aspects of the system, including operation execution times, performance metrics such as response time, number of calls, success/failure rates, and specific events such as hook execution, middleware, and LLM calls. When the agent (acting as the Subject) triggers observability events, the ObservabilityProvider is automatically notified.

The interface defines three main methods: record_metric() to collect numerical metrics, create_span() to create tracking records (spans), and end_span() to finalize these records. These methods allow the provider to capture real-time telemetry and performance data, providing insights into system behavior without directly interfering with the core logic. The ObservabilityProvider can observe not only the agent itself, but also other parts of the system (hooks, middleware) that use these interfaces to report monitoring data.

Snippet 1.2: Subject Notificando Observers (Agent)

The Agent notifies the ObservabilityProvider using the Observer Pattern. When it resolves a user, it creates a span with create_span(), then calls end_span() to finalize it and record_metric() to record performance metrics.

This is the Observer Pattern because:
1. The ObservabilityProvider (Observer) is registered with the Agent.
2. The Agent (Subject) automatically notifies the Observer about events.
3. The Observer receives notifications transparently without knowing implementation details.

The Agent "publishes" observability data that the Provider "subscribes" to for monitoring, a classic example of the Observer pattern where the agent notifies observers about important events.

Snippet 1.3: Multiple Notification Points

Yes, the Agent acts as the Subject and the ObservabilityProvider as the Observer. The Agent is the one that "sends" or "notifies" events, while the ObservabilityProvider is the one that "listens" and receives these notifications.

In this excerpt, I identified 3 notification points:
1. Span creation - when a tool starts executing (create_span)
2. End of span - when the tool finishes executing (end_span)
3. Metric recording - when performance data is saved (record_metric)

These points represent specific moments when the Agent communicates information to the ObservabilityProvider about what is happening in the system, following the Observer pattern. The Agent is responsible for triggering these notifications, and the ObservabilityProvider receives and processes this information for monitoring purposes.

7. Registry Pattern

STRATEGY 1: Identificação via ToolRegistry



Snippet 1.1: ToolRegistry Core

O ToolRegistry implementa o Registry PatternArmazena e gerencia ferramentas em um dicionário onde a chave é o nome da ferramenta (tool.name) e o valor é a própria ferramenta. A chave principal para registrar e recuperar ferramentas é o nome da ferramenta (tool.name). Quando uma ferramenta é registrada via register_local_tool(), ela é armazenada no dicionário self._tools com o nome como chave. Para recuperar uma ferramenta posteriormente, usa-se o método get_tool() passando o nome da ferramenta como parâmetro, que então busca no dicionário usando essa chave. Isso permite que o registry atue como um centro de registro e recuperação de ferramentas, onde cada ferramenta pode ser facilmente acessada pelo seu nome único.

Snippet 1.2: Registrando Ferramentas

O Registry Pattern permite localizar e executar ferramentas dinamicamente por nome porque o ToolRegistry atua como um centro central de registro e recuperação. Quando as ferramentas são registradas no snippet 1.2, elas são armazenadas no dicionário self._tools com o nome da ferramenta como chave. No snippet 1.3, quando é necessário executar uma ferramenta, o código usa await self.get_tool(tool_call.name) para procurar a ferramenta pelo nome armazenado no dicionário. Como o nome da ferramenta é conhecido em tempo de execução (pelo tool_call.name), o registry pode localizar instantaneamente a ferramenta correspondente e executá-la. Isso torna o sistema altamente flexível e extensível - novas ferramentas podem ser adicionadas ao registry e executadas dinamicamente sem precisar modificar o código central, desde que usem nomes únicos para identificação.

Snippet 1.3: Recuperando e Executando do Registry

O Registry Pattern permite localizar e executar ferramentas dinamicamente por nome através de um sistema de armazenamento centralizado. Quando as ferramentas são registradas (como mostrado no snippet 1.2), elas são armazenadas em um dicionário onde a chave é o nome da ferramenta. No snippet 1.3, quando uma ferramenta precisa ser executada, o código usa `await self.get_tool(tool_call.name)` para buscar a ferramenta específica pelo nome que vem no `tool_call`. Isso cria uma ligação dinâmica entre o nome da ferramenta (conhecido em tempo de execução) e a implementação real da ferramenta registrada. Assim, o sistema pode executar qualquer ferramenta previamente registrada apenas conhecendo seu nome, sem precisar saber antecipadamente quais ferramentas estão disponíveis. Essa abordagem torna o sistema altamente modular e extensível - novas ferramentas podem ser adicionadas ao registry e automaticamente tornam-se disponíveis para execução, simplificando a integração de novas funcionalidades.

STRATEGY 2: Identificação via ComponentManager

Snippet 2.1: ComponentManager Registry
O ComponentManager usa o Registry Pattern para gerenciar componentes de UI por ID criando um armazenamento centralizado no atributo self.components que é um dicionário onde a chave é o component_id e o valor é o objeto RichComponent. Quando um componente é emitido via método emit(), ele é registrado no dicionário com seu ID como chave. Depois, quando precise ser recuperado, basta usar o método get_component(component_id) que busca no dicionário usando esse ID.

O registry permite que componentes sejam localizados e gerenciados de forma eficiente por meio de seus IDs únicos, proporcionando um sistema de gerenciamento centralizado que facilita a atualização, substituição e recuperação de componentes. Além disso, o ComponentManager mantém um histórico de atualizações e uma árvore de componentes para tracking completo do ciclo de vida dos componentes. Assim, o Registry Pattern torna possível gerenciar uma coleção dinâmica de componentes de UI de forma organizada e eficiente, permitindo acesso rápido por ID e controle completo do estado dos componentes.

8. Builder Pattern

Como SystemPromptBuilder usa Builder Pattern para construir prompts complexos incrementalmente?


O SystemPromptBuilder usa o Builder Pattern para construir prompts complexos incrementalmente ao dividir a construção do prompt em etapas bem definidas. A implementação `DefaultSystemPromptBuilder` mostra exatamente como isso funciona: primeiro adiciona partes básicas como instruções gerais ("You are a helpful AI assistant."), depois incorpora contexto do usuário ("You are assisting {user.username}."), em seguida inclui informações sobre as ferramentas disponíveis ("You have access to {len(tools)} tools:"), e finalmente adiciona diretrizes de comportamento.

This incremental process allows different Builder implementations to create different representations of the same complex prompt while maintaining the same build process. The pattern allows each part of the prompt to be built separately and combined flexibly, enabling different combinations of elements to create customized prompts for different scenarios without having to rewrite the entire build process each time.

The Agent uses the Builder Pattern to build prompts in multiple steps sequentially and flexibly. First, it calls the `system_prompt_builder` to create the basic prompt with user information and available tools. Then, if an `llm_context_enhancer` is configured, it applies an additional enhancement step to the prompt using the context of the current conversation.


Como o Agent usa o Builder Pattern para construir prompts em múltiplas etapas?"


This approach allows the agent to combine different prompt builders incrementally: the first builder creates the base prompt with static context (user, tools), and the second builder (enhancer) enhances this prompt with dynamic conversation context (current message, history). This demonstrates the power of the Builder Pattern: it allows the same building process (prompt creation) to generate different final representations through additional building steps, keeping the code organized and extensible.

9. Dependency Injection
STRATEGY 1: Identificação via Agent Constructor

Snippet 1.1: Agent Constructor (DI Container)


"Quantas dependências são injetadas no Agent?"
"Por que isso é Dependency Injection e não criação direta?"



The Agent receives 17 dependencies injected into the constructor, such as llm_service, tool_registry, user_resolver, etc. This is Dependency Injection because the Agent does not create these dependencies internally – they are passed from outside by the code that instantiates the agent.

The advantage of DI is that the Agent does not need to know how each dependency is created, it facilitates testing with mocks, allows greater flexibility, and promotes low coupling. The Agent simply stores the dependencies as attributes, following the single responsibility principle and making the system more modular and maintainable.

Snippet 1.2: Usando Dependências Injetadas

The Agent uses its injected dependencies without knowing their concrete implementations because all dependencies follow abstract interfaces defined in the application itself. When the Agent calls `self.user_resolver.resolve_user()` or `self.tool_registry.get_schemas()`, it simply invokes methods defined by the interfaces (UserResolver, ToolRegistry) without worrying about how those methods are concretely implemented.

This works because DI provides concrete implementations of the interfaces when the Agent is created. For example, a `DatabaseUserResolver` or `MemoryUserResolver` can be injected, but the Agent doesn't need to know which one was used – it simply calls the expected methods. This abstraction allows different implementations to be easily swapped (e.g., using a different resolver for production vs. testing) while keeping the Agent code intact, promoting low coupling and greater testability.


STRATEGY 2: Identificação via Tool Constructor


Snippet 2.1: RunSqlTool com DI

RunSqlTool does not create its own SqlRunner because this would violate the Dependency Injection principle, creating coupling between the tool and a specific implementation. If RunSqlTool created the SqlRunner internally, it would be tightly coupled to a single database implementation.

SqlRunner injection makes it easier to switch databases because you only need to inject a different SqlRunner implementation (for example, a MySQLSqlRunner or PostgreSQLSqlRunner) instead of modifying the tool's code. This allows the same RunSqlTool to work with different database backends simply by changing the injected SqlRunner implementation, keeping the tool's logic intact. This promotes high modularity and testability, since we can test the tool with different SqlRunner implementations without altering its code.