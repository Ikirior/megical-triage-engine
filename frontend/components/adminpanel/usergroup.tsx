'use client';

import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "../singlebutton/singlebutton"
import {UserPlus2 } from "lucide-react"
import UserSection from "./usersection"
import cell from "./cell"
import AddUser from "./add_user"
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

    const [state, setState] = useState({creatingUser: false})

    let cellNodes = params.users.values().map(
        // For each cell object
        (cellElement: cell, i) => 
        {
            return <UserSection cell={cellElement} key={'user-'+cellElement.cpf}/>
        }
    ).toArray();

    let keys = Object.keys(params?.users?.at(0) ?? {}).sort().map((element, i) => <div key={'key-'+i}>{element}</div>)

    return (
        <div className={styles.userspanel}>

            <section className={styles.usergroup}>
                <h2>{params.title}</h2>
                <div className={styles.content}>
                    {...keys}
                </div>
                <hr/>
                <div>
                    {...cellNodes}
                    {
                        state.creatingUser &&
                        <UserSection cell={{
                            id:'',
                            cpf:'000.000.000-00',
                            name: 'Dr. Anne',
                            email: 'example@example.com',
                            rg: '00.000.000-0',
                            role: params.title.toLocaleLowerCase(),
                            specialization: 'Dermatology',
                            created_at: new Date().toString()
                        }} newUser={true}/>
                    }
                </div>
            </section>
            <div className={styles.actions}>
                <SingleButton icon={<UserPlus2/>} text="Add User" action={() => addUser(setState)}/>
            </div>
        </div>
    )
}