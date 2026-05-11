# suporter
Suporter available app 1.0

Sistema de disponibilidade de técnicos de atendimento.

---

## Estrutura

```
tech-dashboard/
├── app.py                        # Aplicação Flask principal
├── schema.sql                    # Schema MySQL + dados de exemplo
├── requirements.txt
├── .env.example                  # Modelo de variáveis de ambiente
├── static/
│   └── css/style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── supervisor/
    │   └── dashboard.html
    └── tecnico/
        └── status.html
```

## Login de exemplo (dados de seed)

 Tipo        ID  Senha
 Supervisor  1   1234  
 Técnico     1   1234  
 Técnico     2   1234  

## Rotas

 Rota                                        Método        Descrição                         
 `/`                                         GET           Redireciona conforme sessão       
 `/login`                                    GET, POST     Página de login                   
 `/logout`                                   GET           Encerra sessão                    
 `/supervisor`                               GET           Dashboard do supervisor           
 `/supervisor/tecnico/adicionar`             POST          Adiciona técnico                  
 `/supervisor/tecnico/<id>/editar`           POST          Edita técnico                     
 `/supervisor/tecnico/<id>/deletar`          POST          Remove técnico                    
 `/tecnico`                                  GET           Tela do técnico logado            
 `/tecnico/status`                           POST          Atualiza status/chamados (AJAX)   
 `/api/tecnicos`                             GET           JSON com todos os técnicos        
