'use client';

import { useState } from "react";
import PatientGroup from "./patientgroup";
import GetPatient from "../../services/patientregistry/get_patient";
import { SearchIcon } from "lucide-react";
import { patient } from "../../types/Patient";
import SingleButton from "../shared/singlebutton/singlebutton";
import ResponseManager from "@/utils/responsemanager";

export default function SearchPatient()
{
    const [usersState, setUsers] = useState([] as patient[]);
    return <>
       <form>
        <label htmlFor="cpf_search">Search by CPF:</label>
        <input type="text" name="cpf_search" id="cpf_search" placeholder="000.000.000-00" pattern="\d{3}.\d{3}.\d{3}-\d{2}" />
        <SingleButton icon={<SearchIcon/>} formAction={async (initialState, args) => {
            const res = await GetPatient(args);
            if(res.content)
               setUsers([res.content])
            return res;
        }} text="Search" backgroudColor="transparent" submit/>
      </form>
      <PatientGroup title='' users={usersState} setUsers={setUsers}/>
    </>
}