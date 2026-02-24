import PathBar from "@/components/pathbar/pathbar";
import GetQeuePatients from "@/components/triagesheet/getQueuePatients";
import TriagePanel from "@/components/triagesheet/triagepanel";
import { queueObj } from "@/components/triagesheet/types";

export default async function Page() {

  const patientQueue = await GetQeuePatients();
  return (<>
    <PathBar path="Triage Panel"></PathBar>
    {
      patientQueue.content ?
      <TriagePanel queue={patientQueue.content as queueObj[]}/> :
      patientQueue.msg
    }
  </>
  );
}
