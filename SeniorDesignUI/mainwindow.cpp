#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QLabel>
#include <QFont>
#include <QPixmap>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
    this->setWindowTitle("Senior Design");
    centralWidget = new QWidget(this);
    this->setCentralWidget( centralWidget );
    layout = new QVBoxLayout( centralWidget );

    QLabel *label = new QLabel(this);
    label->setText("Spectrogram");
    label->setAlignment(Qt::AlignCenter);
    QFont font = label->font();
    font.setPointSize(30);
    font.setBold(true);
    label->setFont(font);

    QLabel *picture = new QLabel(this);
    QPixmap pixmap("/home/radar/Documents/Example Spectrograms/Earthquake/04010005_1582046023_Raw_0.png");
    picture->setPixmap(pixmap);
    picture->show();

    QLabel *fall = new QLabel(this);
    fall->setText("Fall Detected");
    fall->setAlignment(Qt::AlignCenter);
    font = fall->font();
    font.setPointSize(50);
    font.setBold(true);
    fall->setStyleSheet("QLabel { background-color : red; color : black; }");
    fall->setFont(font);

    layout->addWidget(label, 0, Qt::AlignCenter);
    layout->addWidget(picture, 0, Qt::AlignCenter);
    layout->addWidget(fall);

    centralWidget->setLayout(layout);

}

MainWindow::~MainWindow() {
    delete ui;
}
