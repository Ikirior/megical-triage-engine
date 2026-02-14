import styles from '@/components/triagesheet/triagesheet.module.css'
import Topic from './topic'
import Field from './field'

export default function TriageSheet()
{
    return (
        <div className={styles.sheet}>
            <h1 style={{'fontSize': "1.6em", "marginLeft": "4px"}}>Triage Sheet</h1>
            <Topic name="Identification"/>
            <Field name='ID' value='Will Rodriguez'/>
            <Field name='ID' value='Will Rodriguez'/>
            <Field name='ID' value='Will Rodriguez'/>
            <Field name='ID' value='Will Rodriguez'/>

            <Topic name="Essentials"/>
            <Field name='ID' value='Will Rodriguez'/>
            <Field name='ID' value='Will Rodriguez'/>

            <Topic name="Observations"/>
            <Field name='ID' value='Will Rodriguez'/>
            
            <Topic name="Complementary Analysis with AI"/>
        </div>
    )
}