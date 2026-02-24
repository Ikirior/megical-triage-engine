# Megical: Triage Engine

*Megical* (Medical + Magical) Triage Engine (MTE) is a web application meant to assist with facilitating the medical workflow at community health centers.

## How does it help?

MTE provides an automated workflow for 3 different roles involved in the attendance process, as well as a system admin. It can assist with:

- **A simple and organized workflow** divided by steps. Receptionists register patients, nurses fill in triage data within 3 separate phases, and doctors finish the attendance. Simple and practical.
- **Automatic queue handling**. Have patients be sent automatically to nurses and doctors without manual inspection. In case of any issues, get back to the phase the triage was left.
- **An Agentic AI-Integrated internal assistant (MedGemma)**, that receives patient information, medical attendance registered history and data written to the Service Sheet to help nurses and doctors make more assertive decisions. Have it assist with the medical flow in providing questions and suggestions to nurses, as well as in summarizing data for doctors: <u>all without the need for any prompts</u>!

A detailed flowchart can be seen in the [documentation]().

## Inspiration

## User Roles

All in all, the system roles are simple and have specific tasks and panels. The table below shows their primary abilities, without going into too much detail.

<table>
    <tr>
        <th>User Role</th>
        <th>What can you do?</th>
    </tr>
    <tr>
        <td>Receptionist</td>
        <td>
            <ul>
                <li>Register patients;</li>
                <li>Update patients;</li>
                <li>Search for patients;</li>
                <li>Send patients to the triage queue.</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Nurse</td>
        <td>
            <ul>
                <li>View triage queue;</li>
                <li>Start triages;</li>
                <li>Continue unfinished triages;</li>
                <li>Send Service Sheets to the doctor queue.</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Doctor</td>
        <td>
            <ul>
                <li>View doctor queue;</li>
                <li>Start and finish attendance.</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Admin</td>
        <td>
        <ul>
            <li>Create system users;</li>
            <li>View system users;</li>
            <li>Delete system users;</li>
            <li>Update system users.</li>
            </ul>
        </td>
    </tr>
</table>

The `nurse` and `doctor` roles get access to panels with a Service Sheet they can interact with. Service Sheets are documents that carry information collected throughout the process, from the reception all the way to the doctor attendance. 

## General Workflow

> PS: all images shown are examples only. They don't reflect real scenarios.

### Admin Panel

The flow starts with the admin panel.
This is a trusted manager who will register each and every user within the system.

INSERT IMAGE

### Patient Registry

Next up, the receptionist is able to register new patients, edit their data and send them to the triage queue.

INSERT IMAGE

### Triage Panel

The triage panel is where most functionalities are.

INSERT IMAGE

To the left, a collapsible sidepanel shows the **triage queue**. You can check when users arrived, as well as their names. To the top, we can see users that haven't had their triage start yet. Below, there are unfished triages that can be continued. You can select the one desired to view the Service Sheet and start or continue their triage.

To the right, another sidepanel can be seen. It is merely a helper, and displays information on the current step for the nurse to follow. 

In the middle, the Service Sheet can be found. It displays fields that can be copied and, depending on the phase (step), edited.

To the bottom, we can view two buttons: one to the left corner and another one to the right.
The one on the left is always used to move on to the next phase, and requires certain data to have been filled in the Service Sheet / Triage Sheet. The one on the right allows you to add new fields with extra data to the **Essentials** section. This means you can create your custom fields, each with a key and value.

The workflow runs with the following steps:

0. Choose triage to continue.
1. Fill in the **Essentials** and **Observations** sections. You may add custom fields to the **Essentials** section. Once done, click on **Generate Questions** to move on to step 2.
2. The **agentic AI** will make use of the data present in the Service Sheet this far, but also of patient history. It will then suggest as many questions as it deems necessary to obtain extra information to help with the diagnosis. Each one will be presented in the sheet with a field you can input the answer in. You may also click on the down-side arrow on each question to reveal its reasoning. Once done, click on **Generate Questions** to move on to the next phase.
3. The **agentic AI** will generate an analysis based on the info provided. You may then make final observations in the corresponding field and set a risk color for the risk evaluation. Finally, click on **Send to Queue** to have a doctor receive the Service Sheet.

### Doctor Panel

The Doctor Panel works in a very similar way to the Triage Panel.

INSERT IMAGE

To the left, a sidepanel shows the queue. You may select a patient from the queue to begin their session. You will notice there's an **AI Pre-Consultation Summary** field, in which you'll receive an **AI-Generated** summary to help you have a better understanding of the patient and of the collected information. You may then insert your notes and type in a prescription once finished.

## Technical Notes

## Future Updates

Many different features are envisioned for MTE. They can enhance multiple different parts of the medical process, with updates that make simples changes, in order to enhance user experience, all the way to new functionalities, that help the workflow feel more natural and precise.

A few updates could be included in a list of possible future changes:

- **An import sheet feature**: importing the Service Sheet from a file could help with specific scenarios, such as with migrating data to the system. An AI could be used to extract information from photos or pdfs and insert them correctly within the system's Service Sheet format.
- **An export sheet feature**: exporting the Service Sheet could help with allowing users to share and print Service Sheets, according to normal user constraints.