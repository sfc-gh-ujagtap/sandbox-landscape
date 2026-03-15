'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';

interface DashboardData {
  ordersSummary: Array<{
    ORDER_MONTH: string;
    ORDER_COUNT: number;
    TOTAL_REVENUE: number;
    UNIQUE_CUSTOMERS: number;
  }>;
  nations: Array<{
    NATION: string;
    TOTAL_REVENUE: number;
    CUSTOMER_COUNT: number;
  }>;
  priorities: Array<{
    PRIORITY: string;
    ORDER_COUNT: number;
    TOTAL_REVENUE: number;
  }>;
  parts: Array<{
    PART_NAME: string;
    PART_TYPE: string;
    TOTAL_QUANTITY: number;
    TOTAL_REVENUE: number;
  }>;
  recentOrders: Array<{
    O_ORDERKEY: number;
    O_ORDERDATE: string;
    CUSTOMER_NAME: string;
    O_TOTALPRICE: number;
    O_ORDERSTATUS: string;
    O_ORDERPRIORITY: string;
  }>;
}

const COLORS = ['#6b7aa3', '#7eb89a', '#e08a80', '#b88585', '#8fa7b8', '#d4b48a'];

const formatCurrency = (value: number) => 
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value);

const formatNumber = (value: number) => 
  new Intl.NumberFormat('en-US').format(value);

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedYear, setSelectedYear] = useState<string>('');

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
        } else {
          setData(data);
          const years = [...new Set(data.ordersSummary.map((o: { ORDER_MONTH: string }) => 
            new Date(o.ORDER_MONTH).getFullYear()
          ))].sort((a, b) => Number(b) - Number(a));
          setSelectedYear(String(years[0]));
        }
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-50">
        <div className="animate-spin rounded-full h-8 w-8 border-2 border-slate-200 border-t-slate-400"></div>
        <span className="ml-3 text-slate-500 font-light">Loading data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-50">
        <Card className="w-96 border-slate-200 bg-white shadow-sm">
          <CardHeader>
            <CardTitle className="text-slate-700 font-medium">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-500">{error}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!data) return null;

  const totalRevenue = data.ordersSummary.reduce((sum, o) => sum + o.TOTAL_REVENUE, 0);
  const totalOrders = data.ordersSummary.reduce((sum, o) => sum + o.ORDER_COUNT, 0);
  const totalCustomers = data.nations.reduce((sum, n) => sum + n.CUSTOMER_COUNT, 0);
  const avgOrderValue = totalRevenue / totalOrders;

  const years = [...new Set(data.ordersSummary.map(o => new Date(o.ORDER_MONTH).getFullYear()))].sort((a, b) => b - a);
  
  const filteredData = data.ordersSummary.filter(o => 
    new Date(o.ORDER_MONTH).getFullYear() === Number(selectedYear)
  );

  const chartData = data.ordersSummary.map(o => ({
    ...o,
    month: new Date(o.ORDER_MONTH).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
  }));

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50">
      <div className="max-w-7xl mx-auto px-6 py-10 space-y-8">
        {/* Header */}
        <div className="border-b border-slate-100 pb-6">
          <h1 className="text-2xl font-semibold text-black tracking-tight">
            Sales Dashboard
          </h1>
          <p className="text-sm text-slate-400 mt-1">TPC-H sample data analytics</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <Card className="bg-gradient-to-br from-indigo-50 to-indigo-100 border-none shadow-sm hover:shadow-lg transition-all duration-300">
            <CardHeader className="pb-1 pt-5">
              <CardDescription className="text-xs uppercase tracking-wider text-indigo-700 font-semibold">Total Revenue</CardDescription>
            </CardHeader>
            <CardContent className="pb-5">
              <p className="text-2xl font-bold text-indigo-900">{formatCurrency(totalRevenue)}</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-emerald-50 to-emerald-100 border-none shadow-sm hover:shadow-lg transition-all duration-300">
            <CardHeader className="pb-1 pt-5">
              <CardDescription className="text-xs uppercase tracking-wider text-emerald-700 font-semibold">Total Orders</CardDescription>
            </CardHeader>
            <CardContent className="pb-5">
              <p className="text-2xl font-bold text-emerald-900">{formatNumber(totalOrders)}</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-amber-50 to-amber-100 border-none shadow-sm hover:shadow-lg transition-all duration-300">
            <CardHeader className="pb-1 pt-5">
              <CardDescription className="text-xs uppercase tracking-wider text-amber-700 font-semibold">Total Customers</CardDescription>
            </CardHeader>
            <CardContent className="pb-5">
              <p className="text-2xl font-bold text-amber-900">{formatNumber(totalCustomers)}</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-rose-50 to-rose-100 border-none shadow-sm hover:shadow-lg transition-all duration-300">
            <CardHeader className="pb-1 pt-5">
              <CardDescription className="text-xs uppercase tracking-wider text-rose-700 font-semibold">Avg Order Value</CardDescription>
            </CardHeader>
            <CardContent className="pb-5">
              <p className="text-2xl font-bold text-rose-900">{formatCurrency(avgOrderValue)}</p>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <Card className="bg-white border-slate-100 shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-black">
                Monthly Revenue Trend
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                  <YAxis tickFormatter={(v) => `$${(v / 1e9).toFixed(1)}B`} tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                  <Tooltip formatter={(value) => formatCurrency(Number(value))} contentStyle={{ border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', color: '#000' }} labelStyle={{ color: '#000' }} />
                  <Line 
                    type="monotone" 
                    dataKey="TOTAL_REVENUE" 
                    stroke="#6b7aa3" 
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 4, fill: '#6b7aa3' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card className="bg-white border-slate-100 shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-black">
                Revenue by Nation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={data.nations} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                  <XAxis type="number" tickFormatter={(v) => `$${(v / 1e9).toFixed(1)}B`} tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="NATION" width={85} tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                  <Tooltip formatter={(value) => formatCurrency(Number(value))} contentStyle={{ border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', color: '#000' }} labelStyle={{ color: '#000' }} />
                  <Bar dataKey="TOTAL_REVENUE" radius={[0, 4, 4, 0]}>
                    {data.nations.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <Card className="bg-white border-slate-100 shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-black">
                Orders by Priority
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={data.priorities}
                    dataKey="ORDER_COUNT"
                    nameKey="PRIORITY"
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={95}
                    paddingAngle={3}
                    label={false}
                  >
                    {data.priorities.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => formatNumber(Number(value))} contentStyle={{ border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', color: '#000' }} labelStyle={{ color: '#000' }} />
                  <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: '12px', color: '#64748b' }} />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card className="bg-white border-slate-100 shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-black">
                Top Parts by Revenue
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={data.parts} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                  <XAxis type="number" tickFormatter={(v) => `$${(v / 1e6).toFixed(1)}M`} tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="PART_NAME" width={140} tick={{ fontSize: 10, fill: '#64748b' }} axisLine={false} tickLine={false} />
                  <Tooltip formatter={(value) => formatCurrency(Number(value))} contentStyle={{ border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', color: '#000' }} labelStyle={{ color: '#000' }} />
                  <Bar dataKey="TOTAL_REVENUE" radius={[0, 4, 4, 0]}>
                    {data.parts.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Recent Orders Table */}
        <Card className="bg-white border-slate-100 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-black">
              Recent Orders
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border border-slate-100 overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="bg-slate-50/50 hover:bg-slate-50/50">
                    <TableHead className="text-xs font-medium text-slate-400 uppercase tracking-wider">Order</TableHead>
                    <TableHead className="text-xs font-medium text-slate-400 uppercase tracking-wider">Date</TableHead>
                    <TableHead className="text-xs font-medium text-slate-400 uppercase tracking-wider">Customer</TableHead>
                    <TableHead className="text-xs font-medium text-slate-400 uppercase tracking-wider text-right">Amount</TableHead>
                    <TableHead className="text-xs font-medium text-slate-400 uppercase tracking-wider">Status</TableHead>
                    <TableHead className="text-xs font-medium text-slate-400 uppercase tracking-wider">Priority</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.recentOrders.slice(0, 8).map((order) => (
                    <TableRow key={order.O_ORDERKEY} className="hover:bg-slate-50/50 border-slate-50">
                      <TableCell className="font-mono text-sm text-slate-500">{order.O_ORDERKEY}</TableCell>
                      <TableCell className="text-sm text-slate-500">{new Date(order.O_ORDERDATE).toLocaleDateString()}</TableCell>
                      <TableCell className="text-sm text-slate-600">{order.CUSTOMER_NAME}</TableCell>
                      <TableCell className="text-sm text-slate-600 text-right font-medium">{formatCurrency(order.O_TOTALPRICE)}</TableCell>
                      <TableCell>
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                          order.O_ORDERSTATUS === 'F' ? 'bg-slate-100 text-slate-600' :
                          order.O_ORDERSTATUS === 'O' ? 'bg-slate-50 text-slate-500' :
                          'bg-white text-slate-400 border border-slate-200'
                        }`}>
                          {order.O_ORDERSTATUS === 'F' ? 'Fulfilled' : 
                           order.O_ORDERSTATUS === 'O' ? 'Open' : 'Pending'}
                        </span>
                      </TableCell>
                      <TableCell className="text-sm text-slate-400">{order.O_ORDERPRIORITY}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        {/* Interactive Analysis */}
        <Card className="bg-white border-slate-100 shadow-sm">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-black">
                Yearly Analysis
              </CardTitle>
              <Select value={selectedYear} onValueChange={(val) => val && setSelectedYear(val)}>
                <SelectTrigger className="w-28 h-8 text-sm border-slate-200 text-slate-600">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {years.map(year => (
                    <SelectItem key={year} value={String(year)}>{year}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
              <div className="lg:col-span-1 space-y-3">
                <div className="p-4 bg-slate-50/50 rounded-lg border border-slate-100">
                  <p className="text-xs uppercase tracking-wider text-slate-400 font-medium">Revenue</p>
                  <p className="text-xl font-semibold text-slate-700 mt-1">
                    {formatCurrency(filteredData.reduce((sum, o) => sum + o.TOTAL_REVENUE, 0))}
                  </p>
                </div>
                <div className="p-4 bg-slate-50/50 rounded-lg border border-slate-100">
                  <p className="text-xs uppercase tracking-wider text-slate-400 font-medium">Orders</p>
                  <p className="text-xl font-semibold text-slate-700 mt-1">
                    {formatNumber(filteredData.reduce((sum, o) => sum + o.ORDER_COUNT, 0))}
                  </p>
                </div>
              </div>
              <div className="lg:col-span-3">
                <ResponsiveContainer width="100%" height={200}>
                  <AreaChart data={filteredData.map(o => ({
                    ...o,
                    month: new Date(o.ORDER_MONTH).toLocaleDateString('en-US', { month: 'short' })
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                    <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                    <YAxis tickFormatter={(v) => `$${(v / 1e9).toFixed(1)}B`} tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                    <Tooltip formatter={(value) => formatCurrency(Number(value))} contentStyle={{ border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', color: '#000' }} labelStyle={{ color: '#000' }} />
                    <Area 
                      type="monotone" 
                      dataKey="TOTAL_REVENUE" 
                      stroke="#7eb89a" 
                      strokeWidth={2}
                      fill="url(#colorRevenue)" 
                    />
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#7eb89a" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#7eb89a" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center py-6 border-t border-slate-100">
          <p className="text-xs text-slate-400">
            Data refreshed from Snowflake
          </p>
        </div>
      </div>
    </div>
  );
}
