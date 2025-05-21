import {
    Page,
    PageSection,
    FileUpload,
    Tabs,
    Tab,
} from "@patternfly/react-core";
import { Grid, Input, Select } from "react-spreadsheet-grid";
import { useState } from "react";
import "@patternfly/react-core/dist/styles/base.css";
import { useTranslation } from "react-i18next";

export const App: React.FC = () => {
    const { t } = useTranslation();

    const [activeTabKey, setActiveTabKey] = useState<number>(0);
    const [rows, setRows] = useState([]);

    return (
        <Page>
            <PageSection>
                <FileUpload />
                {/* <Tabs
                    activeKey={activeTabKey}
                    onSelect={(_, i) => setActiveTabKey(i)}
                >
                    <Tab eventKey={0} title={t("input.tabs.file-upload")}>
                    </Tab>
                    <Tab eventKey={1} title={t("input.tabs.manual-input")}>
                        Users 2
                    </Tab>
                </Tabs> */}
                <Grid
                    columns={[]}
                    rows={rows}
                    // getRowKey={(row) => row.id}
                />
            </PageSection>
        </Page>
    );
};

export default App;
