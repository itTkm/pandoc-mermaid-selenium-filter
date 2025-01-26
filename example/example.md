# Testing Mermaid Filter

Here's a simple flowchart example:

```mermaid
graph TD
    A[Start] --> B{Condition}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
```

\newpage

Here's a sequence diagram example:

```mermaid
sequenceDiagram
    participant Browser
    participant Server
    participant Database

    Browser->>Server: Send Request
    Server->>Database: Execute Query
    Database-->>Server: Return Result
    Server-->>Browser: Send Response
```

\newpage

Here's a class diagram example:

```mermaid
classDiagram
    class Animal {
        +name: string
        +age: int
        +makeSound()
    }
    class Dog {
        +breed: string
        +bark()
    }
    class Cat {
        +color: string
        +meow()
    }
    Animal <|-- Dog
    Animal <|-- Cat
```

\newpage

Here's a architecture diagram example:

```mermaid
architecture-beta
    group api(cloud)[API]

    service db(database)[Database] in api
    service disk1(disk)[Storage] in api
    service disk2(disk)[Storage] in api
    service server(server)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db
```

\newpage

Here's a architecture diagram with [@iconify-json/logos](https://icon-sets.iconify.design/logos/) icons example:

```mermaid
architecture-beta
    group api(logos:aws-lambda)[API]

    service db(logos:aws-aurora)[Database] in api
    service disk1(logos:aws-glacier)[Storage] in api
    service disk2(logos:aws-s3)[Storage] in api
    service server(logos:aws-ec2)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db
```

\newpage

Here's a architecture diagram with [@iconify-json/mdi](https://icon-sets.iconify.design/mdi/) icons example:

```mermaid
architecture-beta
    group api(mdi:api)[API]

    service db(mdi:database)[Database] in api
    service disk1(mdi:harddisk)[Storage] in api
    service disk2(mdi:harddisk)[Storage] in api
    service server(mdi:server)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db
```
