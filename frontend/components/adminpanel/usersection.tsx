import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "../singlebutton/singlebutton"
import { Trash2Icon, SaveIcon, UserPlus2Icon } from "lucide-react"
import cell from "./cell"
import DeleteUser from "./del_user"
import UpdateUser from "./update_user";
import AddUser from "./add_user";

type usersection_params = {
    cell?: cell,
    newUser?: boolean,
    role?: string
}

export default function UserSection(params: usersection_params)
{
    let node_id = params.cell?.id.toWellFormed() ?? 'new';

    return (
        <form className={styles.usersection}>
            <div className={styles.content}>
                
                    <input type="text" name="id" id={node_id+'id'} value={params.cell?.id} placeholder="---" readOnly/>
                    <input type="text" name="rg" id={node_id+'rg'} defaultValue={params.cell?.rg} placeholder="00.000.000-0" pattern="\d{2}.\d{3}.\d{3}-\d"/>
                    <input type="text" name="cpf" id={node_id+'cpf'} defaultValue={params.cell?.cpf} placeholder="000.000.000-00" pattern="\d{3}.\d{3}.\d{3}-\d{2}"/>
                    <input type="text" name="name" id={node_id+'name'} defaultValue={params.cell?.name} placeholder="Dr. Anne" pattern="([a-zA-Z]|\s|\.)+" />
                    <input type="email" name="email" id={node_id+'email'} defaultValue={params.cell?.email} placeholder="example@example.com"/>
                    <input type="text" name="specialization" id={node_id+'specialization'} defaultValue={params.cell?.specialization} placeholder="Dermatology"/>
                    <input type="text" name="role" id={node_id+'role'} value={params.role ?? params.cell?.role} readOnly placeholder="---"/>
                    <input type="text" name="created_at" id={node_id+'created_at'} value={params.cell?.created_at} placeholder="---" readOnly/>
                    
            </div>
            <div className={styles.sectionbuttons}>
                {
                    !params.newUser && 
                    <>
                        <SingleButton icon={<Trash2Icon/>} backgroudColor="#ff5145" submit={true} formAction={DeleteUser}/>
                        <SingleButton icon={<SaveIcon/>} backgroudColor="#5eff79" submit={true} formAction={UpdateUser}/>
                    </>
                }
                {
                    params.newUser && 
                    <>
                        <SingleButton icon={<UserPlus2Icon/>} text='Save User' backgroudColor="#dcff5e" submit={true} formAction={AddUser}/>
                    </>
                }
            </div>
        </form>
    )
}