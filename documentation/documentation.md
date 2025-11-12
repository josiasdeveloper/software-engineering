# Evidências - padrões de projeto


## Padrão de projeto Strategy 

O padrão Strategy define uma família de algoritmos(estratégias), encapsula cada uma delas e as torna intercambiáveis sem alterar o código do cliente.

Objetivo: Criar uma Strategy para cada variante e fazer com que o método delegue o algoritmo para uma instância de Strategy, ou seja, parametrizar os algoritmos usados e tornar uma classe "aberta" a novos algoritmos.


![alt text](image-1.png)



# Como o projeto Vanna utiliza o padrão strategy

![alt text](image-2.png)

## UserResolver:

```python
class UserResolver(ABC):
    @abstractmethod
    async def resolve_user(self, request_context: RequestContext) -> User:
        pass

```

 Interface, onde define "como resolver o usuário", mas não implementa nada. Possui um metodo abstrato resolve_user, que deve obrigatoriamente ser implementado por qualquer classe concreta que herde de UserResolver. 

 A classe Agent não implementa esse método, ela apenas recebe uma estratégia concreta de resolução de usuário através de injeção de dependência.

## ConversationStore

```python
class ConversationStore(ABC):
    @abstractmethod
    async def create_conversation(...):
        pass
```


UserResolver é uma interface implementada como uma classe abstrata. Ela define o contrato para resolver o usuário, através do método abstrato. Esse método não é implementado na classe base, e qualquer classe que herde de UserResolver deve obrigatoriamente fornecer sua própria implementação.


O padrão implementado é o que o Strategy exige:

* Uma família de comportamentos
* Cada comportamento é definido por uma interface
* A implementação é decidida depois

---

#  3. A classe Agent depende das interfaces, não das implementações

 A classe Agent não cria estratégias. Elea recebe estratégias prontas, exatamente como o Strategy define.
 A figura abaixo representa o trecho do construtor da classe, evidenciando que recebe tais estrategias e delega a responsabilidades pra tais classes abstratas.

![alt text](image-2.png)

Analisando oscomentário encontrado na classe, fica evidente que o mecanismo de resolver o usuário é totalmente desacoplado do Agent. Isso significa que o comportamento pode ser trocado por outra estratégia — JWT, cookies, headers, OAuth, etc. — sem modificar o código do Agent, já que ele depende apenas da interface UserResolver.

O mesmo padrão se aplica às classes ConversationStore e LlmService: ambas são plugáveis, seguem contratos abstratos e permitem substituir a estratégia em tempo de execução, mantendo o Agent fechado para modificação e aberto para extensão.

Comentario encontrado no projeto:

![alt text](image-3.png)

---


## Padrão de projeto Observer 

O padrão Observer define uma relação de dependência um-para-muitos entre objetos. Quando um objeto, conhecido como Subject (Sujeito), muda seu estado, todos os seus dependentes, conhecidos como Observers (Observadores), são notificados e atualizados automaticamente.

Objetivo: Permitir que um objeto (o Subject) notifique uma lista de objetos dependentes (os Observers) sobre qualquer mudança de estado, sem que o Subject precise saber quem são ou como eles irão reagir. Isso promove um baixo acoplamento entre o Sujeito e seus Observadores.

# Como o projeto Vanna utiliza o padrão strategy

No projeto Vanna, o padrão Observer é implementado através do sistema de LifecycleHook.

    - O Subject (Sujeito) é a classe Agent. Ela é o componente central cujo ciclo de vida de processamento de mensagens é "observado".
    - A interface do Observer (Observador) é a classe abstrata LifecycleHook.


# LifecycleHook: A interface do "Observer"

A classe LifecycleHook define o "contrato" que qualquer observador concreto deve seguir. Ela estabelece os métodos (eventos) que o Agent irá "notificar". Qualquer classe que queira "ouvir" os eventos do Agent (como um sistema de log, um verificador de cotas, etc.) pode herdar de LifecycleHook e implementar esses métodos.

```python
class LifecycleHook(ABC):
    async def before_message(self, user: User, message: str) -> Optional[str]:
        return None

    async def after_message(self, conversation: Conversation) -> None:
        pass

    async def before_tool(self, tool: Tool, context: ToolContext) -> None:
        pass
        
    async def after_tool(self, result: ToolResult) -> Optional[ToolResult]:
        return None
    
```

A classe Agent atua como o Subject. Ela faz duas coisas principais que caracterizam o padrão:

1. Registro de Observadores (Attachment): Em seu construtor, o Agent recebe e armazena uma lista de seus observadores (lifecycle_hooks), permitindo que componentes externos se registrem.

![alt text](image-6.png)

2. Notificação dos Observadores (Notify): Durante seu ciclo de vida (no método _send_message), o Agent itera sobre sua lista de lifecycle_hooks e os notifica nos momentos apropriados, chamando os métodos definidos pela interface do Observer.  A figura abaixo evidencia a notificação do evento.


![alt text](image-7.png)

Dentro do loop de ferramentas, notifica "before_tool".

![alt text](image-8.png)


NOtifica também o "after_tool" e por fim, notifica No final, notifica "after_message".

![alt text](image-10.png)

![alt text](image-11.png)


o Agent não sabe quais implementações concretas de LifecycleHook estão em sua lista. Ele apenas sabe que eles são do tipo LifecycleHook e que pode chamar métodos como after_message. Dessa forma permite que o sistema seja estendido com novos comportamentos (Observadores Concretos) sem nenhuma modificação no código da classe Agent. Por exemplo, pode-se adicionar um QuotaCheckHook (para verificar cotas de uso) ou um AuditLogHook (para auditoria) simplesmente injetando-os na lista de lifecycle_hooks durante a inicialização do Agent. Isso cumpre perfeitamente o Princípio Aberto/Fechado (Open/Closed Principle), onde o Agent está fechado para modificação, mas aberto para extensão.


## Classe Agent

A classe Agent é de suma importancia para o framework. Ela é responsável por ordenar todo o fluxo de processamento de uma mensagem, desde a recepção até a geração da resposta. No entanto, uma análise de seu construtor revela uma decisão de design crucial, como ilustado no trecho de código abaixo. O Agent não implementa como se comunicar com um LLM, como resolver um usuário ou como armazenar uma conversa. Ele depende de abstrações (interfaces) para esses comportamentos. Esse design é a fundação para os padrões que analisamos.


```python
class Agent:
    def __init__(
        self,
        llm_service: LlmService,
        tool_registry: ToolRegistry,
        user_resolver: UserResolver,
        agent_memory: AgentMemory,
        conversation_store: Optional[ConversationStore] = None,
        # ...
        lifecycle_hooks: List[LifecycleHook] = [],
        llm_middlewares: List[LlmMiddleware] = [],
        # ...
    ) -> None:
        self.llm_service = llm_service
        self.tool_registry = tool_registry
        self.user_resolver = user_resolver
        self.agent_memory = agent_memory
        self.conversation_store = conversation_store
        self.lifecycle_hooks = lifecycle_hooks
        # ...
```