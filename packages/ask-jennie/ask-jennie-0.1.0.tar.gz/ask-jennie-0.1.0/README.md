# Introduction
Jennie as a software package aims to provide platform based protocols through which any developers will be able to store and reuse development related tasks.

The software follows the below structure.

`jennie <stack> <type> <event>`

### Where:

**Stacks** : Stacks are platforms for which protocol aims to run. Currently we have build automation for platforms Angular, Django, Python

**Type** : Each stack may have two types of protocol

- ui-lib : UI Component is made reusable.
- automations : Automation events can be made reusable

**Event** : Supported Events for protocol
    
- Upload
- Download
- Update
- Delete
- Sync
- Create
- Create Readme
- Add Event
- Create API ( Supported for Django only. )

## Supported Protocols for Uploading and Reusing Automations

- **Angular UI library Protocol** the protocol is used to upload and download Angular UI components.

- **Angular Automations Protocol** the protocol is used to upload and download Angular Automations like login-via-google.

- **Django Automation Protocol** the protocol is used to upload and download Django Automations.

- **Ubuntu Server Protocol** the protocol helps developers for deploying andf setting up Ubuntu Servers.


A list of upload software package can be found at : https://automations.ask-jennie.com.
The software can be used only after login, to register continue to https://automations.ask-jennie.com.

### Supported command List

| Command | Usage |
|:-------:|:--:|
| `jennie angular ui-lib download` | Download Angular UI Library from server to local |
| `jennie angular ui-lib upload` | Upload Angular UI Component as library to server |
| `jennie angular ui-lib update` | Update already uploaded Angular UI Component to server |
| `jennie angular ui-lib delete` | Delete angular UI library from server |
| `jennie angular ui-lib sync` | Sync a owners library to local for Angular UI Library |
| `jennie angular ui-lib create-readme` | Create basic readme structure for Angular UI library |
| `jennie angular automations create` | Create basic automation structure for Angular Automations |
| `jennie angular automations add-event` | Add Event to angular Automations |
| `jennie angular automations download` | Download Angular Automations from server to local |
| `jennie angular automations upload` | Upload Angular Automations to server |
| `jennie angular automations update` | Update already uploaded Angular Automations to server |
| `jennie angular automations delete` | Delete angular Automations from server |
| `jennie angular automations sync` | Sync a owners library to local for Angular Automations |
| `jennie angular automations create-readme` | Create basic readme structure for Angular Automations |
| `jennie django automations create` | Create basic automation structure for Django Automations |
| `jennie django automations add-event` | Add Event to Django Automations |
| `jennie django automations download` | Download Django Automations from server to local |
| `jennie django automations upload` | Upload Django Automations to server |
| `jennie django automations update` | Update already uploaded Django Automations to server |
| `jennie django automations delete` | Delete Django Automations from server |
| `jennie django automations sync` | Sync a owners library to local for Django Automations |
| `jennie django automations create-readme` | Create basic readme structure for Django Automations |
| `jennie django automations create-api` | Create basic django api |
| `jennie ubuntu setup lemp` | Install LEMP on ubuntu server ( MYSQL, Nginx, PHP) |
| `jennie ubuntu setup phpmyadmin` | Install PHPMYADMIN on ubuntu server |
| `jennie ubuntu deploy web` | Deploy a web directly on ubuntu server |
| `jennie django deploy django` | Deploy a django project directly on ubuntu server |
