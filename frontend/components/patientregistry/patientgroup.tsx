'use client';

import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "@/components/singlebutton/singlebutton";
import {UserPlus2 } from "lucide-react"
import patient from "./patient";
import { useState } from "react";
import PatientSection from "./patientsection";

type usergroupparams = {
    icon?: any,
    title: string,
    users: patient[],
    setUsers: Function
}

function addUser(setState: Function)
{
    setState({creatingUser: true});
}

export default function PatientGroup(params: usergroupparams)
{
    const [usersState, setUsers] = [params.users, params.setUsers]
    const [state, setState] = useState({creatingUser: false})
    
    let cellNodes = usersState.values().map(
        // For each cell object
        (cellElement: patient, i) => 
        {
            return <PatientSection cell={cellElement} key={'user-'+cellElement.cpf} setUsers={setUsers} usersState={usersState}/>
        }
    ).toArray();

    const KEYS=['Id', 'RG', 'CPF', 'Name', 'Birth Date', 'Address', 'Accompanied?', 'Race', 'Sex', 'Phone Number']
    const keyElements = KEYS.map((element, i) => <div key={'key-'+i}>{element}</div>)

    return (
        <div className={styles.userspanel}>

            <section className={styles.usergroup}>
                <h2>{params.title}</h2>
                <div className={styles.content} style={{borderBottom: "thin #636363 solid"}}>
                    {...keyElements}
                </div>
                <div>
                    {...cellNodes}
                    {
                        state.creatingUser &&
                        <PatientSection newUser={true} role={params.title.toLowerCase()} setUsers={setUsers} usersState={usersState}/>
                    }
                </div>
            </section>
            <div className={styles.actions}>
                <SingleButton icon={<UserPlus2/>} text="Add User" action={() => addUser(setState)}/>
            </div>
        </div>
    )
}