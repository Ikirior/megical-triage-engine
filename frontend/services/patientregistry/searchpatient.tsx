'use client';

import { useState } from "react";
import PatientGroup from "../../components/patientregistry/patientgroup";
import GetPatient from "./get_patient";
import { SearchIcon } from "lucide-react";
import patient from "../../types/Patient";

export default function SearchPatient()
{
    const [usersState, setUsers] = useState([] as patient[]);
    return <>
       <form action={async (args) => {
          const result = await GetPatient(args);
          setUsers([result.content]);
       }}>
        <label htmlFor="cpf_search">Search by CPF:</label>
        <input type="text" name="cpf_search" id="cpf_search" placeholder="000.000.000-00" pattern="\d{3}.\d{3}.\d{3}-\d{2}" />
        <div style={{display: "flex", flexDirection: "row"}}><SearchIcon/><input style={{cursor: "pointer"}} type="submit" value={"Submit"}></input></div>
      </form>
      <PatientGroup title='' users={usersState} setUsers={setUsers}/>
    </>
}