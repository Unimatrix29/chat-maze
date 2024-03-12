# Chat Leap: The LLM Challenge

## Introduction

This document serves as a guideline for team members working on the "Chat Leap: The LLM Challenge" project. It's a retro jump-and-run game with a unique twist: players interact with a Language Learning Model (LLM) like ChatGPT to control the game, but must communicate in a specific tone to execute commands like Left, Right, and Jump.

**German version below.**

## Example Folder Strukture
<pre>
.
├── src                 # All source code will be found in the src folder 
├── docu                # All documentation files will be found in the docu folder 
├── README_TEAM.md      # General information and Guidelines for the team 
└── README.md           # Initial project overview and setup instructions; will evolve to include more detailed documentation for external users
</pre>

## Git Workflow Guidelines

### Issues

Issues are utilized for tracking both feature requests (User Stories) and tasks (Tickets).

#### User Stories

User Stories are collaboratively created by the team to outline features or deliverables. They include a description of the feature, its intended users, and the reasons for its existence. Acceptance criteria define the feature's functionalities and the minimum requirements for acceptance. Each User Story is assigned a unique ID for process automation in GitLab.

**Example User Story:**

>#### 3.2: Frage abändern
>
>**Rolle:** Als HTW-Anwender
>
>**Ich möchte:** die Möglichkeit haben, meine gestellte Frage zu bearbeiten.
>
>**So dass:** ich Anpassungen vornehmen kann, ohne eine komplett neue Suchanfrage zu stellen.
>
>**Akzeptanzkriterien:**
>
>1. Nachdem die Ergebnisse meiner gestellten Frage angezeigt wurden, gibt es eine Option zur Bearbeitung der Frage.
>    
>2. Die Benutzeroberfläche ermöglicht es mir, den Text meiner Frage zu ändern.
>  
>3. Nach der Bearbeitung wird die modifizierte Frage an die KI weitergeleitet.
>  
>4. Die KI verarbeitet die geänderte Frage und generiert eine aktualisierte Suchanfrage.
>
>5. Die neuen Ergebnisse werden direkt auf der Benutzeroberfläche angezeigt.
>  
>6. Die Interaktion respektiert die Sicherheitsrichtlinien und schützt die Privatsphäre des Benutzers.

#### Tickets

Tickets are derived from User Stories to outline specific tasks, forming a to-do list. The ticket title should clearly define the task, while the description can include additional details or implementation plans as needed.

**Example Ticket:**

>#### Integrate JWT Authentication in Frontend
>##### Required Integration Steps
>###### 1. Token Retrieval and Storage
>- Upon a successful login API response, extract the JWT (access token) provided in the response body.
>- Store this token securely on the client side, preferably in the browser's local storage or session storage.
>
>###### 2. Token Usage in API Requests
>- Attach the stored JWT in the `Authorization` header for all authenticated API requests.
>- The header format should be: `Authorization: Bearer <access_token>`.
>- Ensure that this header is included in all requests to endpoints that require authentication.
>
>###### 3. Handling Token Expiry
>- Implement logic to handle scenarios when the token is expired.
>- This could involve redirecting the user to the login page.
>
>###### 4. Error Handling for Authentication Failures
>- Implement error handling for scenarios where the token is invalid, missing, or expired (typically a 401 Unauthorized response).
>- In such cases, prompt the user to re-authenticate.
>
>###### 5. Logout Implementation
>- On user logout, ensure to clear the stored JWT from the client storage.
>- Implement API call for logout if the backend supports an endpoint for invalidating tokens.
>
>##### Backend API Details
>- **Login Endpoint**: `POST /login` - Returns `access_token` and `token_type` upon successful authentication.
>- **Protected Endpoints**: All endpoints that require authentication.

### Branches

Create a new branch for each ticket using the format: `[Ticket ID]-[Ticket Name]`, replacing spaces with hyphens. For instance, for the ticket above, the branch name would be `166-Integrate-JWT-Authentication-in-Frontend`. This naming convention facilitates automation in GitLab. Once your task is completed, initiate a merge request.
### Commits

Commit every significant change, no matter how small, to ensure progress can be accurately tracked and reverted if necessary. Commit messages should be concise yet descriptive, detailing what was done and why. Including the ticket ID in the commit message is encouraged to link the commit to specific tasks.

### Merge Requests (MRs)

When a ticket is completed, create a Merge Request (MR) for your branch. The MR description should summarize the changes and link back to the original ticket for context. Ensure your code adheres to the project's standards and passes all checks before requesting a review.

  
  
  
  
  
  
  





# Deutsche version: 
## Einführung

Dieses Dokument dient als Leitfaden für Teammitglieder, die am Projekt "Chat Leap: Die LLM-Herausforderung" arbeiten. Es handelt sich um ein Retro-Sprung-und-Lauf-Spiel mit einer einzigartigen Wendung: Spieler interagieren mit einem Sprachlernmodell (LLM) wie ChatGPT, um das Spiel zu steuern, müssen jedoch in einem bestimmten Ton kommunizieren, um Befehle wie Links, Rechts und Springen auszuführen.

## Beispiel für die Ordnerstruktur


<pre>
. 
├── src                 # Alle Quellcodes befinden sich im src-Ordner 
├── docu                # Alle Dokumentationsdateien befinden sich im docu-Ordner 
├── README_TEAM.md      # Allgemeine Informationen und Richtlinien für das Team 
└── README.md           # Anfängliche Projektübersicht und Einrichtungsanweisungen; wird erweitert, um detailliertere Dokumentation für externe Nutzer zu beinhalten
</pre>

## Git-Arbeitsablauf-Richtlinien

### Issues

Issues werden sowohl für die Verfolgung von Funktionsanfragen (User Stories) als auch für Aufgaben (Tickets) verwendet.

#### User Stories

User Stories werden gemeinschaftlich vom Team erstellt, um Funktionen oder Liefergegenstände zu umreißen. Sie beinhalten eine Beschreibung der Funktion, ihrer vorgesehenen Benutzer und der Gründe für ihre Existenz. Akzeptanzkriterien definieren die Funktionalitäten der Funktion und die Mindestanforderungen für die Akzeptanz. Jeder User Story wird eine eindeutige ID zugewiesen, um Prozesse in GitLab zu automatisieren.

**Beispiel für eine User Story:**

>#### 3.2: Frage abändern
>
>**Rolle:** Als HTW-Anwender
>
>**Ich möchte:** die Möglichkeit haben, meine gestellte Frage zu bearbeiten.
>
>**So dass:** ich Anpassungen vornehmen kann, ohne eine komplett neue Suchanfrage zu stellen.
>
>**Akzeptanzkriterien:**
>
>1. Nachdem die Ergebnisse meiner gestellten Frage angezeigt wurden, gibt es eine Option zur Bearbeitung der Frage.
>    
>2. Die Benutzeroberfläche ermöglicht es mir, den Text meiner Frage zu ändern.
>  
>3. Nach der Bearbeitung wird die modifizierte Frage an die KI weitergeleitet.
>  
>4. Die KI verarbeitet die geänderte Frage und generiert eine aktualisierte Suchanfrage.
>
>5. Die neuen Ergebnisse werden direkt auf der Benutzeroberfläche angezeigt.
>  
>6. Die Interaktion respektiert die Sicherheitsrichtlinien und schützt die Privatsphäre des Benutzers.

#### Tickets

Aus User Stories abgeleitete Tickets skizzieren spezifische Aufgaben und bilden eine To-do-Liste. Der Titel des Tickets sollte die Aufgabe klar definieren, während die Beschreibung zusätzliche Details oder Implementierungspläne enthalten kann, wie benötigt.

**Beispiel für ein Ticket:**

>#### Integrate JWT Authentication in Frontend
>##### Required Integration Steps
>###### 1. Token Retrieval and Storage
>- Upon a successful login API response, extract the JWT (access token) provided in the response body.
>- Store this token securely on the client side, preferably in the browser's local storage or session storage.
>
>###### 2. Token Usage in API Requests
>- Attach the stored JWT in the `Authorization` header for all authenticated API requests.
>- The header format should be: `Authorization: Bearer <access_token>`.
>- Ensure that this header is included in all requests to endpoints that require authentication.
>
>###### 3. Handling Token Expiry
>- Implement logic to handle scenarios when the token is expired.
>- This could involve redirecting the user to the login page.
>
>###### 4. Error Handling for Authentication Failures
>- Implement error handling for scenarios where the token is invalid, missing, or expired (typically a 401 Unauthorized response).
>- In such cases, prompt the user to re-authenticate.
>
>###### 5. Logout Implementation
>- On user logout, ensure to clear the stored JWT from the client storage.
>- Implement API call for logout if the backend supports an endpoint for invalidating tokens.
>
>##### Backend API Details
>- **Login Endpoint**: `POST /login` - Returns `access_token` and `token_type` upon successful authentication.
>- **Protected Endpoints**: All endpoints that require authentication.

### Branches

Erstellen Sie für jedes Ticket einen neuen Branch mit dem Format: `[Ticket-ID]-[Ticket Name]`, wobei Leerzeichen durch Bindestriche ersetzt werden. Beispielsweise wäre der Name des Branches für das obige Ticket `166-Integrate-JWT-Authentication-in-Frontend`. Diese Benennungskonvention erleichtert die Automatisierung in GitLab. Sobald Ihre Aufgabe abgeschlossen ist, initiieren Sie eine Merge-Anfrage

### Commits

Führen Sie einen Commit für jede signifikante Änderung durch, egal wie klein, um den Fortschritt genau nachverfolgen und bei Bedarf rückgängig machen zu können. Commit-Nachrichten sollten knapp, aber beschreibend sein und darlegen, was getan wurde und warum. Es wird empfohlen, die Ticket-ID in die Commit-Nachricht einzubeziehen, um den Commit mit spezifischen Aufgaben zu verknüpfen.

### Merge-Anfragen (MRs)

Wenn ein Ticket abgeschlossen ist, erstellen Sie eine Merge-Anfrage (MR) für Ihren Branch. Die Beschreibung der MR sollte die Änderungen zusammenfassen und auf das ursprüngliche Ticket verweisen. Stellen Sie sicher, dass Ihr Code den Standards des Projekts entspricht und alle Überprüfungen bestanden hat, bevor Sie eine Überprüfung anfordern.