import React from "react";
import styles from "./UserPanel.module.css";
import { TopBar } from '../../components/topBar/TopBar';
import { Box } from "@mantine/core";

function UserPanel() {
  return (
    <div className={styles.container}>
      <TopBar />
      <div className={styles.content}>
        <div className={styles.headerSection}>
          <div className={styles.title}>User Panel</div>
        </div>
      </div>
    </div>
  );
}

export default UserPanel;