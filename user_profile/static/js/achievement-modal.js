var ACHIEVEMENT_LEVEL_THRESHOLDS = {
    1: {
        'color': "green"
    },
    3: {
        'level': "Bronze",
        'color': "#CD7F32"
    },
    5: {
        'level': "Silver",
        'color': "silver"
    },
    10: {
        'level': "Gold",
        'color': "gold"
    }
}


var ACHIEVEMENT_LOCKED_COLOR = "grey";


function openModal(name, description, icon, defaultIcon, unlockedTimes) {

    let modalBackground = document.getElementById("achievement-modal-background");

    let modal = document.getElementById("achievement-modal");

    let closeButton = modal.getElementsByClassName("close-button")[0];

    modalBackground.addEventListener("click", function(event) {
        if (event.target === modalBackground) {
            closeModal();
        }
    });

    closeButton.addEventListener("click", function() {
        closeModal();
    });

    let modalTitle = modal.getElementsByClassName("achievement-modal-title")[0];
    let modalDescription = modal.getElementsByClassName("achievement-modal-description")[0];
    let achievementCounter = modal.getElementsByClassName("achievement-counter")[0];
    let achievementCounterText = modal.getElementsByClassName("achievement-counter-text")[0];
    let achievementLevel = modal.getElementsByClassName("achievement-level")[0];
    let modalIcon = modal.getElementsByClassName("achievement-modal-icon")[0];
    let modalUnlockInfo = modal.getElementsByClassName("achievement-modal-unlock-info")[0];

    let modalLevels = modal.getElementsByClassName("achievement-modal-level");

    let level = null;

    for (let threshold in ACHIEVEMENT_LEVEL_THRESHOLDS) {
        if (unlockedTimes >= threshold) {
            level = ACHIEVEMENT_LEVEL_THRESHOLDS[threshold];
        }
    }

    modalBackground.style.display = "block";

    if (unlockedTimes < 2) {
        achievementCounter.style.display = "none";
    } else {
        achievementCounter.style.display = "flex";
        achievementCounterText.innerHTML = unlockedTimes;
    }

    if (level !== null && level.level) {
        achievementLevel.style.display = "block";
        achievementLevel.innerHTML = level.level;
        achievementLevel.style.color = level.color;
    } else {
        achievementLevel.style.display = "none";
    }

    if (level) {
        modalIcon.style.borderColor = level.color;
        achievementCounter.style.background = level.color;
    } else {
        modalIcon.style.borderColor = ACHIEVEMENT_LOCKED_COLOR;
        achievementCounter.style.background = ACHIEVEMENT_LOCKED_COLOR;
    }

    modalTitle.innerHTML = name;
    modalDescription.innerHTML = description;

    if (level) {
        modalUnlockInfo.style.color = level.color;
    } else {
        modalUnlockInfo.style.color = ACHIEVEMENT_LOCKED_COLOR;
    }
    
    if (unlockedTimes === 0) {

        modalIcon.src = defaultIcon;
        modalUnlockInfo.innerHTML = "The achievement is not unlocked yet";

    } else {

        let word;

        if (unlockedTimes === 1) {
            word = "time";
        } else {
            word = "times";
        }

        modalIcon.src = icon;
        modalUnlockInfo.innerHTML = `The achievement is unlocked ${unlockedTimes} ${word}`;

    }

    for (let i = 0; i < modalLevels.length; i++) {
        
        let levelName = modalLevels[i].getAttribute("level");

        let levelIcon = modalLevels[i].getElementsByClassName("achievement-modal-icon")[0];
        let levelComment = modalLevels[i].getElementsByClassName("achievement-level-comment")[0];

        for (let threshold in ACHIEVEMENT_LEVEL_THRESHOLDS) {

            if (ACHIEVEMENT_LEVEL_THRESHOLDS[threshold].level && ACHIEVEMENT_LEVEL_THRESHOLDS[threshold].level === levelName) {

                let levelColor = ACHIEVEMENT_LEVEL_THRESHOLDS[threshold].color;

                levelIcon.style.borderColor = levelColor;

                if (unlockedTimes >= threshold) {
                    levelIcon.src = icon;
                } else {
                    levelIcon.src = defaultIcon;
                }

                if (unlockedTimes < threshold) {

                    let timesLeft = threshold - unlockedTimes;

                    let word;

                    if (timesLeft === 1) {
                        word = "time";
                    } else {
                        word = "times";
                    }

                    levelComment.innerHTML = `You need to unlock the achievement ${timesLeft} more ${word} to reach ${levelName.toLowerCase()} level`;
                    
                } else {
                    levelComment.innerHTML = `${levelName} level already reached!`;
                }

            }

        }

    }

}


function closeModal() {
    document.getElementById("achievement-modal-background").style.display = "none";
}
