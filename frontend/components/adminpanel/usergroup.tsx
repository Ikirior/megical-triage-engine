'use client';

import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "@/components/shared/singlebutton/singlebutton";
import {UserPlus2 } from "lucide-react"
import UserSection from "./usersection"
import { cell } from "@/types/Cell";
import { useState } from "react";

type usergroupparams = {
    icon?: any,
    title: string,
    users: cell[]
}

function addUser(setState: Function)
{
    setState({creatingUser: true});
}

export default function UserGroup(params: usergroupparams)
{

    const [usersState, setUsers] = useState(params.users)
    const [state, setState] = useState({creatingUser: false})

    let cellNodes = usersState.values().map(
        // For each cell object
        (cellElement: cell, i) => 
        {
            return <UserSection cell={cellElement} key={'user-'+cellElement.cpf} setUsers={setUsers} usersState={usersState}/>
        }
    ).toArray();

    const KEYS=['Id', 'RG', 'CPF', 'Name', 'E-mail', 'Specialization', 'Role', 'Creation Date']
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
                        <UserSection newUser={true} role={params.title.toLowerCase()} setUsers={setUsers} usersState={usersState}/>
                    }
                </div>
            </section>
            <div className={styles.actions}>
                <SingleButton icon={<UserPlus2/>} text="Add User" action={() => addUser(setState)}/>
            </div>
        </div>
    )
}