import FormComp from "@/components/form/form_comp";
import style from '@/app/login/styles.module.css'
import Message from "@/components/messages/msg";

export default function LoginPage() {
  return (
    <div className={style.form}>
        <h1 className={style.title}>Megical Assistant</h1>
        <FormComp/>
    </div>
  );
}
