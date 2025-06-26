import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AdvancedDashboard:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Titanic Analytics Dashboard")
        self.root.geometry("1800x1200")
        self.root.configure(bg='#1e1e1e')
        
        self.colors = {
            'bg': '#1e1e1e',
            'panel': '#2d2d2d', 
            'accent': '#00d4aa',
            'danger': '#ff6b6b',
            'warning': '#ffa726',
            'info': '#42a5f5',
            'text': '#ffffff',
            'muted': '#9e9e9e'
        }
        
        self.df = pd.read_csv('titanic.csv').dropna()
        self.filtered_df = self.df.copy()
        
        self._setup_styles()
        self._create_interface()
        self.update_all()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Dark.TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('Dark.TNotebook.Tab', background=self.colors['panel'], 
                       foreground=self.colors['text'], padding=[20, 10])
        style.map('Dark.TNotebook.Tab', background=[('selected', self.colors['accent'])])
        
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['text'])
        style.configure('Dark.TCombobox', background=self.colors['panel'], foreground=self.colors['text'])

    def _create_interface(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_header(main_frame)
        self._create_notebook(main_frame)

    def _create_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg'], height=80)
        header.pack(fill=tk.X, pady=(0, 10))
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="🚢 TITANIC ANALYTICS DASHBOARD", 
                              font=("Arial", 24, "bold"), fg=self.colors['accent'], 
                              bg=self.colors['bg'])
        title_label.pack(side=tk.LEFT, pady=20)
        
        export_btn = tk.Button(header, text="📊 Export Data", command=self.export_data,
                              bg=self.colors['accent'], fg='white', font=("Arial", 10, "bold"),
                              relief=tk.FLAT, padx=20)
        export_btn.pack(side=tk.RIGHT, pady=20, padx=10)
        
        refresh_btn = tk.Button(header, text="🔄 Refresh", command=self.update_all,
                               bg=self.colors['info'], fg='white', font=("Arial", 10, "bold"),
                               relief=tk.FLAT, padx=20)
        refresh_btn.pack(side=tk.RIGHT, pady=20)

    def _create_notebook(self, parent):
        self.notebook = ttk.Notebook(parent, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self._create_overview_tab()
        self._create_analysis_tab()
        self._create_data_tab()

    def _create_overview_tab(self):
        overview_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(overview_frame, text="📈 OVERVIEW")
        
        self._create_control_panel(overview_frame)
        self._create_stat_cards(overview_frame)
        self._create_overview_charts(overview_frame)

    def _create_control_panel(self, parent):
        control_panel = tk.Frame(parent, bg=self.colors['panel'], height=100)
        control_panel.pack(fill=tk.X, padx=5, pady=5)
        control_panel.pack_propagate(False)
        
        tk.Label(control_panel, text="FILTERS", font=("Arial", 12, "bold"), 
                fg=self.colors['accent'], bg=self.colors['panel']).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self._create_filter_controls(control_panel)

    def _create_filter_controls(self, parent):
        tk.Label(parent, text="Class:", fg=self.colors['text'], 
                bg=self.colors['panel']).grid(row=1, column=0, padx=10, sticky='w')
        self.class_var = tk.StringVar(value="All")
        class_combo = ttk.Combobox(parent, textvariable=self.class_var,
                                  values=["All", "1", "2", "3"], width=8)
        class_combo.grid(row=1, column=1, padx=5)
        class_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        tk.Label(parent, text="Sex:", fg=self.colors['text'], 
                bg=self.colors['panel']).grid(row=1, column=2, padx=10, sticky='w')
        self.sex_var = tk.StringVar(value="All")
        sex_combo = ttk.Combobox(parent, textvariable=self.sex_var,
                                values=["All", "male", "female"], width=8)
        sex_combo.grid(row=1, column=3, padx=5)
        sex_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        tk.Label(parent, text="Age Range:", fg=self.colors['text'], 
                bg=self.colors['panel']).grid(row=1, column=4, padx=10, sticky='w')
        
        self.age_min = tk.Scale(parent, from_=0, to=80, orient=tk.HORIZONTAL, 
                               bg=self.colors['panel'], fg=self.colors['text'], 
                               troughcolor=self.colors['bg'], command=self.apply_filters)
        self.age_min.grid(row=1, column=5, padx=5)
        
        self.age_max = tk.Scale(parent, from_=0, to=80, orient=tk.HORIZONTAL,
                               bg=self.colors['panel'], fg=self.colors['text'],
                               troughcolor=self.colors['bg'], command=self.apply_filters)
        self.age_max.set(80)
        self.age_max.grid(row=1, column=6, padx=5)

    def _create_stat_cards(self, parent):
        stats_frame = tk.Frame(parent, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stat_vars = {}
        stats = ['Total Passengers', 'Survivors', 'Survival Rate', 'Avg Age', 'Avg Fare']
        
        for stat in stats:
            card = tk.Frame(stats_frame, bg=self.colors['panel'], relief=tk.RAISED, bd=2)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
            
            self.stat_vars[stat] = tk.StringVar()
            tk.Label(card, textvariable=self.stat_vars[stat], font=("Arial", 16, "bold"),
                    fg=self.colors['accent'], bg=self.colors['panel']).pack(pady=5)
            tk.Label(card, text=stat, font=("Arial", 10), 
                    fg=self.colors['muted'], bg=self.colors['panel']).pack()

    def _create_overview_charts(self, parent):
        charts_frame = tk.Frame(parent, bg=self.colors['bg'])
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.overview_fig = plt.Figure(figsize=(18, 10), facecolor=self.colors['bg'])
        self.overview_canvas = FigureCanvasTkAgg(self.overview_fig, charts_frame)
        self.overview_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _create_analysis_tab(self):
        analysis_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(analysis_frame, text="🔬 ANALYSIS")
        
        self._create_analysis_controls(analysis_frame)
        self._create_analysis_charts(analysis_frame)

    def _create_analysis_controls(self, parent):
        analysis_controls = tk.Frame(parent, bg=self.colors['panel'], height=80)
        analysis_controls.pack(fill=tk.X, padx=5, pady=5)
        analysis_controls.pack_propagate(False)
        
        tk.Label(analysis_controls, text="ADVANCED ANALYTICS", font=("Arial", 12, "bold"),
                fg=self.colors['accent'], bg=self.colors['panel']).pack(pady=10)
        
        button_frame = tk.Frame(analysis_controls, bg=self.colors['panel'])
        button_frame.pack()
        
        buttons = [
            ("Correlation Heatmap", self.show_correlation),
            ("Survival Analysis", self.survival_analysis),
            ("Age Distribution", self.age_analysis),
            ("Fare Analysis", self.fare_analysis)
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                           bg=self.colors['info'], fg='white', relief=tk.FLAT, padx=15)
            btn.pack(side=tk.LEFT, padx=5)

    def _create_analysis_charts(self, parent):
        self.analysis_fig = plt.Figure(figsize=(14, 8), facecolor=self.colors['bg'])
        self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, parent)
        self.analysis_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_data_tab(self):
        data_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(data_frame, text="📊 DATA")
        
        self._create_data_controls(data_frame)
        self._create_data_table(data_frame)

    def _create_data_controls(self, parent):
        data_controls = tk.Frame(parent, bg=self.colors['panel'], height=60)
        data_controls.pack(fill=tk.X, padx=5, pady=5)
        data_controls.pack_propagate(False)
        
        tk.Label(data_controls, text="DATA EXPLORER", font=("Arial", 12, "bold"),
                fg=self.colors['accent'], bg=self.colors['panel']).pack(side=tk.LEFT, padx=10, pady=15)
        
        search_label = tk.Label(data_controls, text="Search:", fg=self.colors['text'], 
                               bg=self.colors['panel'])
        search_label.pack(side=tk.LEFT, padx=10)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(data_controls, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.search_data)

    def _create_data_table(self, parent):
        tree_frame = tk.Frame(parent, bg=self.colors['bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = list(self.df.columns)
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._populate_tree()

    def apply_filters(self, event=None):
        df = self.df.copy()
        
        if self.class_var.get() != "All":
            df = df[df['Pclass'] == int(self.class_var.get())]
        
        if self.sex_var.get() != "All":
            df = df[df['Sex'] == self.sex_var.get()]
        
        min_age = self.age_min.get()
        max_age = self.age_max.get()
        df = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]
        
        self.filtered_df = df
        self._update_overview()
        self._update_stats()

    def _update_stats(self):
        df = self.filtered_df
        total = len(df)
        survivors = df['Survived'].sum()
        survival_rate = (survivors / total * 100) if total > 0 else 0
        avg_age = df['Age'].mean()
        avg_fare = df['Fare'].mean()
        
        self.stat_vars['Total Passengers'].set(f"{total:,}")
        self.stat_vars['Survivors'].set(f"{survivors:,}")
        self.stat_vars['Survival Rate'].set(f"{survival_rate:.1f}%")
        self.stat_vars['Avg Age'].set(f"{avg_age:.1f}")
        self.stat_vars['Avg Fare'].set(f"£{avg_fare:.2f}")

    def _update_overview(self):
        self.overview_fig.clear()
        df = self.filtered_df
        
        gs = self.overview_fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        self._create_survival_pie_chart(gs, df)
        self._create_class_survival_chart(gs, df)
        self._create_age_distribution_chart(gs, df)
        self._create_sex_class_chart(gs, df)
        self._create_age_fare_scatter(gs, df)
        self._create_embarkation_chart(gs, df)
        
        self.overview_fig.patch.set_facecolor(self.colors['bg'])
        self.overview_canvas.draw()

    def _create_survival_pie_chart(self, gs, df):
        ax1 = self.overview_fig.add_subplot(gs[0, 0])
        survival = df['Survived'].value_counts()
        colors = [self.colors['danger'], self.colors['accent']]
        wedges, texts, autotexts = ax1.pie(survival.values, labels=['Died', 'Survived'], 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Survival Rate', color=self.colors['text'], fontweight='bold')
        ax1.set_facecolor(self.colors['bg'])

    def _create_class_survival_chart(self, gs, df):
        ax2 = self.overview_fig.add_subplot(gs[0, 1])
        class_survival = df.groupby('Pclass')['Survived'].mean()
        bars = ax2.bar(class_survival.index, class_survival.values, 
                      color=[self.colors['danger'], self.colors['warning'], self.colors['info']])
        ax2.set_title('Survival by Class', color=self.colors['text'], fontweight='bold')
        ax2.set_ylabel('Survival Rate', color=self.colors['text'])
        ax2.set_facecolor(self.colors['bg'])
        ax2.tick_params(colors=self.colors['text'])

    def _create_age_distribution_chart(self, gs, df):
        ax3 = self.overview_fig.add_subplot(gs[0, 2:])
        for survived in [0, 1]:
            subset = df[df['Survived'] == survived]
            color = self.colors['accent'] if survived else self.colors['danger']
            ax3.hist(subset['Age'], bins=20, alpha=0.7, color=color, 
                    label='Survived' if survived else 'Died')
        ax3.set_title('Age Distribution by Survival', color=self.colors['text'], fontweight='bold')
        ax3.set_xlabel('Age', color=self.colors['text'])
        ax3.set_ylabel('Count', color=self.colors['text'])
        ax3.legend()
        ax3.set_facecolor(self.colors['bg'])
        ax3.tick_params(colors=self.colors['text'])

    def _create_sex_class_chart(self, gs, df):
        ax4 = self.overview_fig.add_subplot(gs[1, :2])
        sex_class = df.groupby(['Sex', 'Pclass'])['Survived'].mean().unstack()
        sex_class.plot(kind='bar', ax=ax4, color=[self.colors['danger'], self.colors['warning'], self.colors['info']])
        ax4.set_title('Survival by Sex and Class', color=self.colors['text'], fontweight='bold')
        ax4.set_ylabel('Survival Rate', color=self.colors['text'])
        ax4.set_facecolor(self.colors['bg'])
        ax4.tick_params(colors=self.colors['text'])
        ax4.legend(title='Class')

    def _create_age_fare_scatter(self, gs, df):
        ax5 = self.overview_fig.add_subplot(gs[1, 2:])
        for survived in [0, 1]:
            subset = df[df['Survived'] == survived]
            color = self.colors['accent'] if survived else self.colors['danger']
            ax5.scatter(subset['Age'], subset['Fare'], alpha=0.6, c=color, s=30,
                       label='Survived' if survived else 'Died')
        ax5.set_title('Age vs Fare by Survival', color=self.colors['text'], fontweight='bold')
        ax5.set_xlabel('Age', color=self.colors['text'])
        ax5.set_ylabel('Fare', color=self.colors['text'])
        ax5.legend()
        ax5.set_facecolor(self.colors['bg'])
        ax5.tick_params(colors=self.colors['text'])

    def _create_embarkation_chart(self, gs, df):
        ax6 = self.overview_fig.add_subplot(gs[2, :])
        embark_survival = df.groupby('Embarked')['Survived'].agg(['count', 'sum'])
        x = np.arange(len(embark_survival.index))
        width = 0.35
        
        ax6.bar(x - width/2, embark_survival['count'], width, label='Total', color=self.colors['info'])
        ax6.bar(x + width/2, embark_survival['sum'], width, label='Survived', color=self.colors['accent'])
        
        ax6.set_title('Passengers and Survivors by Embarkation Port', color=self.colors['text'], fontweight='bold')
        ax6.set_xlabel('Embarkation Port', color=self.colors['text'])
        ax6.set_ylabel('Count', color=self.colors['text'])
        ax6.set_xticks(x)
        ax6.set_xticklabels(embark_survival.index)
        ax6.legend()
        ax6.set_facecolor(self.colors['bg'])
        ax6.tick_params(colors=self.colors['text'])

    def show_correlation(self):
        self.analysis_fig.clear()
        numeric_cols = self.filtered_df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.filtered_df[numeric_cols].corr()
        
        ax = self.analysis_fig.add_subplot(111)
        im = ax.imshow(corr_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
        
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right', color=self.colors['text'])
        ax.set_yticklabels(corr_matrix.columns, color=self.colors['text'])
        
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                              ha="center", va="center", color="white", fontweight='bold')
        
        ax.set_title('Correlation Heatmap', color=self.colors['text'], fontsize=14, fontweight='bold', pad=15)
        ax.set_facecolor(self.colors['bg'])
        
        cbar = self.analysis_fig.colorbar(im, ax=ax, shrink=0.8)
        cbar.ax.yaxis.set_tick_params(color=self.colors['text'])
        cbar.ax.yaxis.set_ticklabels(cbar.ax.yaxis.get_ticklabels(), color=self.colors['text'])
        
        self.analysis_fig.tight_layout(pad=1.5)
        self.analysis_fig.patch.set_facecolor(self.colors['bg'])
        self.analysis_canvas.draw()

    def survival_analysis(self):
        self.analysis_fig.clear()
        df = self.filtered_df
        
        gs = self.analysis_fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        ax1 = self.analysis_fig.add_subplot(gs[0, 0])
        sex_survival = df.groupby('Sex')['Survived'].mean()
        bars = ax1.bar(sex_survival.index, sex_survival.values, 
                      color=[self.colors['info'], self.colors['accent']])
        ax1.set_title('Survival Rate by Gender', color=self.colors['text'], fontweight='bold')
        ax1.set_ylabel('Survival Rate', color=self.colors['text'])
        ax1.set_facecolor(self.colors['bg'])
        ax1.tick_params(colors=self.colors['text'])
        
        ax2 = self.analysis_fig.add_subplot(gs[0, 1])
        age_bins = pd.cut(df['Age'], bins=5)
        age_survival = df.groupby(age_bins)['Survived'].mean()
        bars = ax2.bar(range(len(age_survival)), age_survival.values, color=self.colors['warning'])
        ax2.set_title('Survival Rate by Age Group', color=self.colors['text'], fontweight='bold')
        ax2.set_ylabel('Survival Rate', color=self.colors['text'])
        ax2.set_xticks(range(len(age_survival)))
        ax2.set_xticklabels([f'{int(interval.left)}-{int(interval.right)}' for interval in age_survival.index], rotation=45)
        ax2.set_facecolor(self.colors['bg'])
        ax2.tick_params(colors=self.colors['text'])
        
        ax3 = self.analysis_fig.add_subplot(gs[1, :])
        fare_bins = pd.qcut(df['Fare'], q=4, precision=0)
        fare_survival = df.groupby(fare_bins)['Survived'].mean()
        ax3.bar(range(len(fare_survival)), fare_survival.values, color=self.colors['danger'])
        ax3.set_title('Survival Rate by Fare Quartile', color=self.colors['text'], fontweight='bold')
        ax3.set_ylabel('Survival Rate', color=self.colors['text'])
        ax3.set_xticks(range(len(fare_survival)))
        ax3.set_xticklabels([f'£{interval.left:.0f}-£{interval.right:.0f}' for interval in fare_survival.index], rotation=45)
        ax3.set_facecolor(self.colors['bg'])
        ax3.tick_params(colors=self.colors['text'])
        
        self.analysis_fig.tight_layout(pad=1.5)
        self.analysis_fig.patch.set_facecolor(self.colors['bg'])
        self.analysis_canvas.draw()

    def age_analysis(self):
        self.analysis_fig.clear()
        df = self.filtered_df
        
        ax = self.analysis_fig.add_subplot(111)
        
        parts = ax.violinplot([df[df['Survived']==0]['Age'].dropna(), 
                              df[df['Survived']==1]['Age'].dropna()], 
                             positions=[1, 2], showmeans=True, showmedians=True)
        
        colors = [self.colors['danger'], self.colors['accent']]
        for pc, color in zip(parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        
        ax.set_title('Age Distribution by Survival Status', color=self.colors['text'], 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Age', color=self.colors['text'])
        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Did not survive', 'Survived'])
        ax.set_facecolor(self.colors['bg'])
        ax.tick_params(colors=self.colors['text'])
        
        self.analysis_fig.tight_layout(pad=1.5)
        self.analysis_fig.patch.set_facecolor(self.colors['bg'])
        self.analysis_canvas.draw()

    def fare_analysis(self):
        self.analysis_fig.clear()
        df = self.filtered_df
        
        gs = self.analysis_fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        ax1 = self.analysis_fig.add_subplot(gs[0, :])
        ax1.boxplot([df[df['Pclass']==1]['Fare'], df[df['Pclass']==2]['Fare'], 
                    df[df['Pclass']==3]['Fare']], labels=['1st Class', '2nd Class', '3rd Class'])
        ax1.set_title('Fare Distribution by Class', color=self.colors['text'], fontweight='bold')
        ax1.set_ylabel('Fare (£)', color=self.colors['text'])
        ax1.set_facecolor(self.colors['bg'])
        ax1.tick_params(colors=self.colors['text'])
        
        ax2 = self.analysis_fig.add_subplot(gs[1, 0])
        ax2.scatter(df['Fare'], df['Age'], c=df['Survived'], cmap='RdYlGn', alpha=0.6)
        ax2.set_title('Fare vs Age (colored by survival)', color=self.colors['text'], fontweight='bold')
        ax2.set_xlabel('Fare (£)', color=self.colors['text'])
        ax2.set_ylabel('Age', color=self.colors['text'])
        ax2.set_facecolor(self.colors['bg'])
        ax2.tick_params(colors=self.colors['text'])
        
        ax3 = self.analysis_fig.add_subplot(gs[1, 1])
        high_fare = df[df['Fare'] > df['Fare'].quantile(0.75)]['Survived'].mean()
        low_fare = df[df['Fare'] <= df['Fare'].quantile(0.25)]['Survived'].mean()
        bars = ax3.bar(['Low Fare\n(Bottom 25%)', 'High Fare\n(Top 25%)'], [low_fare, high_fare],
                      color=[self.colors['danger'], self.colors['accent']])
        ax3.set_title('Survival Rate by Fare Level', color=self.colors['text'], fontweight='bold')
        ax3.set_ylabel('Survival Rate', color=self.colors['text'])
        ax3.set_facecolor(self.colors['bg'])
        ax3.tick_params(colors=self.colors['text'])
        
        self.analysis_fig.tight_layout(pad=1.5)
        self.analysis_fig.patch.set_facecolor(self.colors['bg'])
        self.analysis_canvas.draw()

    def _populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        df_display = self.filtered_df.head(100)
        for _, row in df_display.iterrows():
            self.tree.insert('', 'end', values=list(row))

    def search_data(self, event=None):
        search_term = self.search_var.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if not search_term:
            self._populate_tree()
            return
        
        filtered_data = self.filtered_df[
            self.filtered_df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False)).any(axis=1)
        ]
        
        for _, row in filtered_data.head(100).iterrows():
            self.tree.insert('', 'end', values=list(row))

    def export_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.filtered_df.to_csv(filename, index=False)
            messagebox.showinfo("Export Complete", f"Data exported to {filename}")

    def update_all(self):
        self.apply_filters()
        self._populate_tree()
        self.show_correlation()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedDashboard(root)
    root.mainloop() 