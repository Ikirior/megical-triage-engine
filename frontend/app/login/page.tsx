import FormComp from "@/components/form/form_comp";
import style from '@/app/login/styles.module.css'

export default function LoginPage() {
  return (
    <div className={style.form}>
        <h1 className={style.title}>Megical: Triage Engine</h1>
        <FormComp/>
    </div>
  );
}
