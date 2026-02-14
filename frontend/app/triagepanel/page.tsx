import TriageSheet from "@/components/triagesheet/triagesheet";
import style from '@/app/triagepanel/styles.module.css'
import PathBar from "@/components/pathbar/pathbar";
import MajorButton from "@/components/majorbutton/majorbutton";
import { Send, Rocket, PlusIcon } from "lucide-react";
import SingleButton from "@/components/singlebutton/singlebutton";

export default function Page() {
  return (<>
    <PathBar path="Triage Panel"></PathBar>
    <h1 style={{"margin": "4vh 0 0 2vh", "fontSize": "2em"}}>&lt;Patient&gt;'s Triage Sheet</h1>
    <div className={style.panel}>
        <TriageSheet></TriageSheet>
    </div>
    <nav id="form-actions" className={[style.actions, style.form_actions].join(' ')}>
      <MajorButton icon={<Rocket/>} content="Generate Analysis" ></MajorButton>
      <MajorButton icon={<Send/>} content="Send to Queue" ></MajorButton>

      <div className={style.plus_button}>
        <SingleButton icon={<PlusIcon/>}/>
      </div>
    </nav>
  </>
  );
}
