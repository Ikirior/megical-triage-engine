import DoctorPanel from "@/components/doctorpanel/doctorpanel";
import GetDoctorQueue from "@/services/doctorpanel/getDoctorQueue";
import PathBar from "@/components/shared/pathbar/pathbar";
import GetQeuePatients from "@/services/triagepanel/getQueuePatients";
import { queueObj } from "@/types/types";

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
