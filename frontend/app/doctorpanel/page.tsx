import DoctorPanel from "@/components/doctorpanel/doctorpanel";
import GetDoctorQueue from "@/components/doctorpanel/getDoctorQueue";
import PathBar from "@/components/pathbar/pathbar";
import GetQeuePatients from "@/components/triagesheet/getQueuePatients";
import { queueObj } from "@/components/triagesheet/types";

export default async function Page() {

  const patientQueue = await GetDoctorQueue();
  return (<>
    <PathBar path="Triage Panel"></PathBar>
    {
      patientQueue.content ?
      <DoctorPanel queue={patientQueue.content as queueObj[]}/> :
      patientQueue.msg
    }
  </>
  );
}
