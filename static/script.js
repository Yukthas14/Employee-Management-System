let allEmployees=[]
async function loadDepartments(){
let response=await fetch("/api/departments")
let data=await response.json()
let dropdown=document.getElementById("department")
dropdown.innerHTML=""
data.forEach(dept=>{
dropdown.innerHTML+=`
<option value="${dept.id}">${dept.name}</option>`
})
}

async function loadEmployees(){
let response=await fetch("/api/employees")
let data=await response.json()
allEmployees=data
displayEmployees(data)
}

function displayEmployees(data){
let table=document.getElementById("employeeTable")

table.innerHTML=""
data.forEach(emp=>{
table.innerHTML+=`
<tr>
<td>${emp.id}</td>
<td>${emp.name}</td>
<td>${emp.email}</td>
<td>${emp.department}</td>
<td>${emp.salary}</td>
<td>${emp.joining_date}</td>
<td><button onclick= "deleteEmployee(${emp.id})"> Delete </button></td>
</tr>`
})
}

async function addEmployee(){
let employee={
name:document.getElementById("name").value,
email:document.getElementById("email").value,
department_id:document.getElementById("department").value,
salary:document.getElementById("salary").value,
joining_date:document.getElementById("joiningDate").value
}

await fetch("/api/employees",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(employee)
})
loadEmployees()
}

async function deleteEmployee(id){
await fetch(`/api/employees/${id}`,{
method:"DELETE"
})
loadEmployees()
}

function searchEmployee(){
let keyword=document.getElementById("search").value.toLowerCase()
let filtered=allEmployees.filter(
emp=>
emp.name.toLowerCase().includes(keyword)
)

displayEmployees(filtered)
}
loadDepartments()
loadEmployees()