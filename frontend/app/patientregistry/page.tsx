import style from '@/app/adminpanel/styles.module.css'
import PathBar from "@/components/shared/pathbar/pathbar";
import SearchPatient from '../../services/patientregistry/searchpatient';
export const dynamic='force-dynamic';


export default async function Page() {

  return (<>
    <PathBar path="Home > Patient Registry"></PathBar>
    <div className={style.panel}>
      <h1 style={{"fontSize": "2em"}}>Patient Registry</h1>
      <h2>Register, view and check in patients.</h2>
      <SearchPatient/>
    </div>
  </>
  );
}
