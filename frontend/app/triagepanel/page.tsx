import PathBar from "@/components/shared/pathbar/pathbar";
import GetQeuePatients from "@/services/triagepanel/getQueuePatients";
import TriagePanel from "@/components/triagesheet/triagepanel";
import { queueObj } from "@/types/types";

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
